from ..model import DemoRiskPredictor, ThompsonSamplerTimingPolicy
from .assistant_service import AssistantService, assistant_service
from .behavioral_analysis_service import BehavioralAnalysisService, behavior_service
from .orchestration_service import OrchestrationService
from .content_detection_service import default_content_detection_service
from .exceptions import ContentDetectionFlaggedError

default_orchestrator = OrchestrationService(
    assistant_service=AssistantService(),
    behavior_service=BehavioralAnalysisService(),
    risk_predictor=DemoRiskPredictor(),
    timing_policy=ThompsonSamplerTimingPolicy(),
)

__all__ = [
    "AssistantService",
    "BehavioralAnalysisService",
    "OrchestrationService",
    "default_orchestrator",
    "assistant_service",
    "behavior_service",
    "default_content_detection_service",
    "ContentDetectionFlaggedError"
]
