import logging

import openai
from typing import List

from ..config import settings
from ..dto import Goal, UserProfile, DailyMetric

logger = logging.getLogger(__name__)

DEFAULT_COACH_NAME = "Laura"

FUNCTIONS = [
    {
      "name": "suggest_goal",
      "description": "Propose a precise new goal based on today's metrics and risk score.",
      "parameters": {
        "type": "object",
        "properties": {
          "metric": {"type": "string", "enum": ["steps", "active_minutes", "sleep_hours"]},
          "target_value": {"type": "number"},
          "rationale": {"type": "string"}
        },
        "required": ["metric", "target_value", "rationale"]
      }
    },
    {
      "name": "coach_message",
      "description": "Chat message to child giving feedback, tips and encouragement.",
      "parameters": {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "required": ["message"]
      }
    }
]


class AssistantService:
    """Service for managing assistants."""

    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    def _build_system_context(assistant_name: str):
        return f"""
        You are {assistant_name}, a friendly, empathetic youth health coach (age-appropriate tone, no weight-shaming).
        Use evidence-based behaviour-change techniques: goal-setting, self-monitoring, feedback, praise.
        When suggesting goals, only pick ONE, make it SMART (don't mention this explicitly, instead summarize how it's smart in a conversational, simple manner), 
        and tie it to the child's interests. You should always address the child by their first name in your message.
        """

    @staticmethod
    def _build_user_context(
        user_profile: UserProfile,
        metrics: DailyMetric,
        goals: List[Goal],
        risk: float
    ) -> str:
        """
        Build context for the assistant based on daily metrics and goals.
        """
        goal_lines = "\n".join([f"- {g.description} (status: {g.status})" for g in goals])
        risk = "unknown" if not risk else f"{risk:.2%}"

        return f"""
        Child info:
        - Name: {user_profile.first_name}
        - Age: {user_profile.age}
        - Sex: {user_profile.sex}
        - Preferences: {', '.join(user_profile.preferences)}
        - Health conditions: {', '.join(user_profile.health_conditions)}
        - Height (cm): {user_profile.height_cm}
        - Weight (kg): {user_profile.weight_kg}
        
        Child metrics today:
        - Steps: {metrics.steps}
        - Active minutes: {metrics.active_minutes}
        - Calories in: {metrics.calories_in}
        - Sleep hours: {metrics.sleep_hours}

        Current goals:
        {goal_lines or 'None'}

        Risk score: {risk}
        """

    def create_recommendation(
        self,
        user_profile: UserProfile,
        metrics: DailyMetric,
        goals: List[Goal],
        risk: float
    ) -> str:
        """
        Get recommendations from the assistant based on daily metrics and goals.
        """
        assistant_name = user_profile.coach_profile.name if user_profile.coach_profile else DEFAULT_COACH_NAME

        system_content = self._build_system_context(assistant_name)
        user_content = self._build_user_context(
            user_profile=user_profile,
            metrics=metrics,
            goals=goals,
            risk=risk
        )

        logger.info(f"User content: {user_content}")

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            functions=FUNCTIONS,
            function_call="none",
            temperature=0.8,
            user=user_profile.user_id,
            seed=42,
        )

        logger.info(f"Assistant response: {resp}")

        return resp.choices[0].message.content


# TODO: replace with DI
assistant_service = AssistantService()
