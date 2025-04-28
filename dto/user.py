from pydantic import BaseModel, Field
from typing import Optional, List


class CoachProfile(BaseModel):
    """Minimal coach metadata."""
    id: str = Field(..., example="UUID")
    name: str = Field(..., example="Coach Name")
    description: Optional[str] = Field(None, example="A friendly health coach.")
    instructions: Optional[str] = Field(None, example="You are a friendly health coach.")
    model: Optional[str] = Field(None, example="gpt-4o-mini")
    assistant_id: Optional[str] = Field(None, example="UUID")


class UserProfile(BaseModel):
    """Minimal user metadata (COPPA‑safe)."""
    user_id: str = Field(..., example="UUID")
    first_name: str = Field(..., example="John")
    age: int = Field(..., ge=2, le=19, example=14)
    sex: Optional[str] = Field(None, example="female")
    height_cm: Optional[float] = Field(None, example=160.0)
    weight_kg: Optional[float] = Field(None, example=55.0)
    preferences: List[str] = Field(default_factory=list, example=["soccer", "carrots"])
    health_conditions: List[str] = Field(default_factory=list, example=["asthma", "diabetes"])
    coach_profile: Optional[CoachProfile] = None
    caretaker_id: Optional[str] = Field("UNKNOWN", example="UUID as a string")
