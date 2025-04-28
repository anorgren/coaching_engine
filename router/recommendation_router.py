from typing import List

from fastapi import HTTPException, APIRouter

from ..service import default_orchestrator
from ..dto import DailyMetric, Recommendation, UserProfile, Goal


router = APIRouter(
    prefix="/recommendation",
    tags=["recommendation"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"},
    },
)


@router.post("/")
def create_recommendation(profile: UserProfile, daily_metrics: DailyMetric, goals: List[Goal]) -> Recommendation:
    """Primary endpoint consumed by Orchestrator or Assistants function call."""

    # Very basic validation of request payload
    if not profile or not daily_metrics:
        raise HTTPException(status_code=400, detail="missing profile or metrics")

    if profile.user_id != daily_metrics.user_id:
        raise HTTPException(status_code=400, detail="user_id mismatch between profile and metrics")

    return default_orchestrator.create_daily_recommendation(profile, daily_metrics, goals)


@router.get("/{recommendation_id}", response_model=Recommendation)
def get_recommendation(recommendation_id: str) -> Recommendation:
    """Get an existing recommendation by ID."""
    raise HTTPException(status_code=501, detail="Not implemented")
