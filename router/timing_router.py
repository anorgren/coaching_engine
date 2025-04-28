from typing import Optional

from fastapi import APIRouter

from ..dto import TimingPolicyType, TimingPolicyUpdate, TimingPolicyResponse
from ..model import TimingPolicyFactory

router = APIRouter(
    prefix="/timing",
    tags=["timing"],
    responses={404: {"description": "Not found"}},
)


@router.put("/")
def update_policy_reward(request: TimingPolicyUpdate) -> None:
    """Update the reward for a specific timing policy."""
    policy = TimingPolicyFactory.create_timing_policy(request.policy_name, request.user_id)
    policy.update(request.hour, request.reward)


@router.get("/{policy_type}/", response_model=TimingPolicyResponse)
def get_timing_for_policy(
        policy_type: TimingPolicyType,
        user_id: Optional[str] = None,
) -> TimingPolicyResponse:
    """Get the timing for a specific policy type and user."""
    policy = TimingPolicyFactory.create_timing_policy(policy_type, user_id)
    hour = policy.select_hour()

    return TimingPolicyResponse(
        policy_type=policy_type,
        hour=hour,
        user_id=user_id,
    )
