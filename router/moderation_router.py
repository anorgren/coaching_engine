from fastapi import APIRouter
from openai.types import Moderation

from ..service import default_content_detection_service

router = APIRouter(
    prefix="/moderation",
    tags=["moderation"],
    responses={404: {"description": "Not found"}},
)


@router.post("/textContentDetection/", response_model=Moderation)
def detect_text_content(content: str) -> Moderation:
    """Get the timing for a specific policy type and user."""
    return default_content_detection_service.detect_content(content)
