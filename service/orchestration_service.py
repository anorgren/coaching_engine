import logging
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from .exceptions import ContentDetectionFlaggedError
from ..model import RiskPredictor, TimingPolicy
from ..dto import BehavioralRecommendation, Recommendation, UserProfile, DailyMetric, Goal
from ..service import AssistantService, BehavioralAnalysisService
from .content_detection_service import default_content_detection_service

logger = logging.getLogger(__name__)


class OrchestrationService:
    def __init__(
        self,
        assistant_service: AssistantService,
        risk_predictor: RiskPredictor,
        timing_policy: TimingPolicy,
        behavior_service: BehavioralAnalysisService,
    ):
        """Initialize the orchestration service.

        Args:
            assistant_service (AssistantService): The assistant service to use.
            risk_predictor (RiskPredictor): The risk predictor to use.
            timing_policy (TimingPolicy): The timing policy to use.
        """
        self.assistant_service = assistant_service
        self.risk_predictor = risk_predictor
        self.timing_policy = timing_policy
        self.behavior_service = behavior_service
        self.content_detection_service = default_content_detection_service

    def create_daily_recommendation(
        self,
        user_profile: UserProfile,
        daily_metric: DailyMetric,
        goals: List[Goal],
    ) -> Recommendation:
        """
        Create a recommendation for the user based on their profile and daily metrics.

        Args:
            user_profile (UserProfile): The user's profile.
            daily_metric (DailyMetric): The user's daily metrics.
            goals (list): The user's goals.

        Returns:
            Recommendation: The recommendation for the user.
        """

        logger.info(f"Creating recommendation - user_id={user_profile.user_id}, metrics={daily_metric}")

        goal_text = "\n".join(f"{goal.description}" for goal in goals)
        moderation_response = self.content_detection_service.detect_content(goal_text)

        if moderation_response.flagged:
            # TODO: should emit async event for followup w/ caregiver (maybe internal staff too) about content of goals
            logger.warning(
                f"Content flagged - user_id={user_profile.user_id}, content={goal_text}, "
                f"categories={moderation_response.categories}"
            )
            raise ContentDetectionFlaggedError(
                content=goal_text,
                flagged_categories=[
                    cat for cat in moderation_response.categories.__fields__
                    if getattr(moderation_response.categories, cat)
                ],
            )

        # calculate risk
        risk = self.risk_predictor.score(user_profile)

        # get recommendation from assistant
        recommendation = self.assistant_service.create_recommendation(
            user_profile=user_profile,
            metrics=daily_metric,
            goals=goals,
            risk=risk,
        )

        # get time to send the recommendation
        send_time = self.timing_policy.select_hour()

        logger.info(
            f"Recommendation created - user_id={user_profile.user_id}, recommendation={recommendation}, "
            f"risk={risk}, send_time={send_time}"
        )

        return Recommendation(
            id=str(uuid4()),
            user_id=user_profile.user_id,
            message=recommendation,
            send_time=send_time,
            created_at=datetime.now()
        )

    def check_for_concerning_behaviors(
        self,
        user_profile: UserProfile,
        daily_metrics: List[DailyMetric],
    ) -> Optional[BehavioralRecommendation]:
        """
        Check for concerning behaviors based on daily metrics over some time period.

        Args:
            user_profile (UserProfile): The user's profile.
            daily_metrics (List[DailyMetric]): The user's daily metrics.

        Returns:
            BehavioralRecommendation: The recommendation for the user.
        """
        logger.info(f"Checking for concerning behaviors - user_id={user_profile.user_id}, metrics={daily_metrics}")

        # analyze behavior
        recommendation = self.behavior_service.analyze_aggregate_user_metrics(
            user_profile=user_profile,
            daily_metrics=daily_metrics
        )

        logger.info(f"Behavioral recommendation - user_id={user_profile.user_id}, recommendation={recommendation}")

        return recommendation
