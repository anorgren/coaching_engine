"""DTOs for metrics."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DailyMetric(BaseModel):
    """Daily metrics for a user."""
    user_id: str
    date: datetime
    steps: int
    active_minutes: int
    calories_in: int
    sleep_hours: float
    weight_kg: Optional[float] = None
    emotion: Optional[str] = None

    class Config:
        from_attributes = True
