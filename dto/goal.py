import enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class GoalType(str, enum.Enum):
    """Type of goal."""
    ACTIVE_MINUTES = "active_minutes"
    HEALTHY_MEALS = "healthy_meals"
    NUTRITION = "nutrition"
    STEPS = "steps"
    SLEEP = "sleep"
    MOOD = "mood"
    OTHER = "other"


class GoalPeriod(str, enum.Enum):
    """Period of goal."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"


class Goal(BaseModel):
    """Goal for a user."""
    id: str
    user_id: str
    description: str
    target_value: str
    target_unit: str
    metric: str
    status: str = Field("active", pattern="^(active|met|expired)$")
    start_date: datetime = Field(default_factory=datetime.utcnow)
    type: Optional[GoalType] = None
    period: GoalPeriod = Field(GoalPeriod.DAILY)

    class Config:
        from_attributes = True
