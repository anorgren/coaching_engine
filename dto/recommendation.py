"""DTOs for recommendations."""
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional


class Recommendation(BaseModel):
    """Response returned to the LLM or client app.
    
    TODO:
    - Should this handle "badges" or should that be handled by the client?
    - Should this be split into multiple messages?
    """
    id: str
    message: str
    send_time: int  # hour indicating when the msg should be sent
    badge: Optional[str] = None  # gold / silver / bronze

    created_at: datetime  # when the recommendation was created by the orchestration system

    class Config:
        from_attributes = True


class BehavioralRecommendation(BaseModel):
    """Recommendation for a user based on their behavior."""
    id: str
    user_id: str
    caretaker_id: str
    alert_title: str
    summary: str
    suggested_step: str
    triggered_rules: list[str]  # list of rule IDs that triggered this recommendation

    generated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
