from typing import List


class RecommendationError(Exception):
    """Base class for all recommendation-related exceptions."""
    pass


class ContentDetectionError(Exception):
    """Base class for all content detection-related exceptions."""
    pass


class ContentDetectionFlaggedError(ContentDetectionError):
    """Exception raised when content is flagged by the content detection service."""
    def __init__(self, content: str, flagged_categories: List[str]):
        self.content = content
        self.flagged_categories = flagged_categories
        super().__init__(f"Content flagged for violating policies: {flagged_categories}")


class FlaggedGoalError(RecommendationError):
    """Exception raised when a recommendation is flagged."""
    def __init__(self, recommendation_id: str, reason: str):
        self.recommendation_id = recommendation_id
        self.reason = reason
        super().__init__(f"Recommendation {recommendation_id} flagged: {reason}")