import logging
from typing import List, Optional

from fastapi import HTTPException, APIRouter

from ..dto import BehavioralRecommendation
from ..service import default_orchestrator
from ..dto import DailyMetric, UserProfile

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/behavior",
    tags=["behavior"],
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=Optional[BehavioralRecommendation],
    responses={
        204: {
            "description": "No behavioral recommendation found",
            "headers": {"x-empty-response": {"description": "No behavior detected"}},
        }
    },
)
def create_behavioral_analysis(profile: UserProfile, metrics: List[DailyMetric]):
    """Primary endpoint consumed by Orchestrator or Assistants function call."""

    # basic validation of request payload
    if not metrics:
        raise HTTPException(status_code=400, detail="missing metrics")

    if len(metrics) < 7:
        raise HTTPException(status_code=400, detail="At least 7 days of metrics are required")

    behavior_rec = default_orchestrator.check_for_concerning_behaviors(
        user_profile=profile,
        daily_metrics=metrics,
    )

    logger.info(f"Behavioral recommendation created: user_id={profile.user_id}, rec={behavior_rec}")

    return behavior_rec


@router.get("/{recommendation_id}", response_model=BehavioralRecommendation)
def get_behavioral_recommendation(recommendation_id: str):
    """Get an existing recommendation by ID."""
    return HTTPException(status_code=501, detail="Not implemented")
