"""Service to analyze user behavior and provide insights."""
import json
import logging
import uuid

import openai
import pandas as pd

from typing import List, Optional

from ..config import settings
from ..dto import BehavioralRecommendation, DailyMetric, UserProfile

CAREGIVER_FUNCTIONS = [
    {
        "name": "issue_alert",
        "description": (
            "Generate a concise, plain-language alert for the caretaker summarising "
            "concerning behaviour patterns, why they matter, and a suggested next step."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "alert_title": {"type": "string"},
                "summary": {"type": "string"},
                "suggested_step": {"type": "string"}
            },
            "required": ["alert_title", "summary", "suggested_step"]
        }
    }
]

SYSTEM_CONTENT = """
You are an expert pediatric dietitian helping a caregiver interpret multiple days of health data.
Be friendly, concise, supportive, and avoid blame. 
"""
NO_ACTION_RESPONSE = "no action needed"

# TODO: these should be configurable and not constants
INCREASED_ACTIVITY_STEP_THRESHOLD = 1500
DECREASED_CALORIE_THRESHOLD = 0.25
THREE_DAY_LOW_CALORIE_THRESHOLD = 1200
LOW_SLEEP_THRESHOLD_HOURS = 6
SLEEP_DEBT_DAYS = 4

logger = logging.getLogger(__name__)


class BehavioralAnalysisService:
    def __init__(self):
        """
        Initializes the Behavioral Analysis Service.
        """
        self.openai_client: openai.OpenAI = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def analyze_aggregate_user_metrics(
        self,
        user_profile: UserProfile,
        daily_metrics: List[DailyMetric],
    ) -> Optional[BehavioralRecommendation]:
        """
        Analyzes the collected behavioral data over .

        If a concerning pattern is detected, it generates a recommendation for the user.
        If no concerning pattern is detected, it returns None.

        Args:
            user_profile (UserProfile): The user's profile.
            daily_metrics (List[DailyMetric]): The user's daily metrics.

        Returns:
            Optional[BehavioralRecommendation]: The recommendation for the user or None if no action is needed.
        """
        rule_violations = self._check_red_flag_rules(daily_metrics)

        logger.info(f"Internal rule violations - user_id={user_profile.user_id}, violations={rule_violations}")

        user_content = self._build_context(
            user=user_profile,
            metrics=daily_metrics,
            rule_ids=rule_violations
        )

        messages = [
            {"role": "system", "content": SYSTEM_CONTENT},
            {"role": "user", "content": user_content}
        ]

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            functions=CAREGIVER_FUNCTIONS,
            function_call="auto",
            temperature=0.8,
            user=user_profile.caretaker_id if user_profile.caretaker_id else user_profile.user_id,
        )
        msg = response.choices[0].message

        # If no action needed, return null
        if msg.content and NO_ACTION_RESPONSE in msg.content.lower():
            logger.info(f"No action needed - user_id={user_profile.user_id}")
            return None

        payload = json.loads(msg.function_call.arguments)

        alert_title = payload.get("alert_title")
        summary = payload.get("summary")
        suggested_step = payload.get("suggested_step")

        logger.info(
            f"Alert generated - user_id={user_profile.user_id}, violations={rule_violations}, "
            f"alert_title={alert_title}, summary={summary}, suggested_step={suggested_step}"
        )

        return BehavioralRecommendation(
            id=str(uuid.uuid4()),
            user_id=user_profile.user_id,
            caretaker_id=user_profile.caretaker_id,
            alert_title=alert_title,
            summary=summary,
            suggested_step=suggested_step,
            triggered_rules=rule_violations,
        )

    @staticmethod
    def _build_context(user: UserProfile, metrics: List[DailyMetric], rule_ids: List[str]) -> str:
        """Build the context for the assistant."""
        # convert to dataframe for easier manipulation
        df = pd.DataFrame(m.model_dump() for m in metrics)
        df.sort_values(by="date", ascending=False, inplace=True)

        trailing_seven_days = df.head(7)

        # TODO: add weight values if present
        trends = {
            "avg_steps": int(trailing_seven_days["steps"].mean()),
            "avg_kcal":  int(trailing_seven_days["calories_in"].mean()),
            "avg_sleep_hours": round(trailing_seven_days["sleep_hours"].mean(), 1),
            # "weight_change_kg": trailing_seven_days["weight_kg"].iloc[0] - trailing_seven_days["weight_kg"].iloc[-1]
        }

        trend_str = ", ".join(f"{k.replace('_',' ')}: {v}" for k, v in trends.items())

        return f"""
        Caretaker id: {user.caretaker_id or 'Caretaker'}
        Child: {user.first_name}, {user.age} years old
        7-day behaviour summary: {trend_str}
        Triggered rules: {', '.join(rule_ids) or 'None'}
        
        If Triggered rules is not 'None' or you identify other concerning patterns, call the function `issue_alert`
        with a helpful, empathetic title, a 1-3-sentence summary, and one concrete suggested next step.
        If no concerning pattern, respond with: {{"message":"No action needed"}}
        """

    @staticmethod
    def _check_red_flag_rules(metrics: List[DailyMetric]) -> List[str]:
        """
        Check if the user is seemingly engaged in risky behavior that requires immediate intervention.

        TODO: make this more dynamic and avoid hardcoding thresholds. Investigate ML approaches or a rule engine.
        """
        violations = []

        # convert to dataframe for easier manipulation
        df = pd.DataFrame(m.model_dump() for m in metrics)
        df.sort_values(by="date", ascending=False, inplace=True)

        # check if theres a big 7 day drop in calories and a big increase in activity
        if len(df) > 7:
            most_recent_week = df.head(7)
            most_recent_week_mean_steps = most_recent_week["steps"].mean()
            most_recent_week_mean_calories = most_recent_week["calories_in"].mean()

            trailing_week = df.head(14).tail(7)
            trailing_week_mean_steps = trailing_week["steps"].mean()
            trailing_week_mean_calories = trailing_week["calories_in"].mean()

            if trailing_week_mean_calories > 0:
                drop = (trailing_week_mean_calories - most_recent_week_mean_calories) / trailing_week_mean_calories

                if (
                    drop > DECREASED_CALORIE_THRESHOLD
                    and most_recent_week_mean_steps > (trailing_week_mean_steps + INCREASED_ACTIVITY_STEP_THRESHOLD)
                ):
                    violations.append("CAL_DROP_ACTIVITY_RISE")

        # check if there are persistent low-calorie days over any 3 day period
        low_cal_flags = (df.head(5)["calories_in"] < THREE_DAY_LOW_CALORIE_THRESHOLD)
        has_low_cal_period = low_cal_flags.rolling(3).sum().any()

        if has_low_cal_period:
            violations.append("LOW_CAL_PERSIST")

        # check if user is getting persistently poor sleep
        num_days_poor_sleep = (df.tail(7)["sleep_hours"] < LOW_SLEEP_THRESHOLD_HOURS).sum()

        if num_days_poor_sleep >= SLEEP_DEBT_DAYS:
            violations.append("SLEEP_DEBT")

        return violations


# TODO: replace with DI
behavior_service = BehavioralAnalysisService()
