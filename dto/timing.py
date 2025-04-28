import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TimingPolicyType(str, enum.Enum):
    THOMPSON_SAMPLING = "thompson_sampling"


class TimingPolicyUpdate(BaseModel):
    """Timing update for a user."""
    policy_type: TimingPolicyType
    hour: int
    reward: int
    user_id: Optional[str] = None
    user_ip: Optional[str] = None
    event_id: Optional[str] = None
    event_timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True


class TimingPolicyResponse(BaseModel):
    """Response for a timing policy request."""
    policy_type: TimingPolicyType
    hour: int
    user_id: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
