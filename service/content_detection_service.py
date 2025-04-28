import logging
import re
from typing import Dict, List, Pattern, Set

import openai
from openai.types import Moderation
from openai.types.moderation import Categories, CategoryScores

from ..config import settings

logger = logging.getLogger(__name__)


class ContentDetectionService:
    CATEGORY_PATTERNS: Dict[str, List[Pattern]] = {
        "harassment": [
            re.compile(r"\b(stupid|idiot|dumb|moron)\b", re.IGNORECASE),
            re.compile(r"\byou suck\b", re.IGNORECASE),
        ],
        "harassment/threatening": [
            re.compile(r"\bkill you\b", re.IGNORECASE),
            re.compile(r"\bI’ll (beat|smash) you\b", re.IGNORECASE),
        ],
        "hate": [
            # targeted at protected classes
            re.compile(r"\b(nigg[ae]r|faggot|kikes)\b", re.IGNORECASE),
            re.compile(r"\bkill all (women|blacks|jews)\b", re.IGNORECASE),
        ],
        "hate/threatening": [
            re.compile(r"\b(exterminate|annihilat)e ((women|blacks|jews))\b", re.IGNORECASE),
        ],
        "illicit": [
            re.compile(r"\bhow to shoplift\b", re.IGNORECASE),
            re.compile(r"\bbuild a bomb\b", re.IGNORECASE),
        ],
        "illicit/violent": [
            re.compile(r"\bwhere to get a gun\b", re.IGNORECASE),
            re.compile(r"\bkill for hire\b", re.IGNORECASE),
        ],
        "self-harm": [
            re.compile(r"\b(I want to die|cut myself|starve myself)\b", re.IGNORECASE),
        ],
        "self-harm/intent": [
            re.compile(r"\bI am going to kill myself\b", re.IGNORECASE),
        ],
        "self-harm/instructions": [
            re.compile(r"\bhow to kill myself\b", re.IGNORECASE),
            re.compile(r"\bways to cut yourself\b", re.IGNORECASE),
        ],
        "sexual": [
            re.compile(r"\bsexual act\b", re.IGNORECASE),
            re.compile(r"\bexplicit sex\b", re.IGNORECASE),
        ],
        "sexual/minors": [
            re.compile(r"\bunder 18\b.*\bsex\b", re.IGNORECASE),
        ],
        "violence": [
            re.compile(r"\b(murder|assault|rape)\b", re.IGNORECASE),
        ],
        "violence/graphic": [
            re.compile(r"\b(gore|blood spurt|disembowel)\b", re.IGNORECASE),
        ],
    }

    def __init__(self):
        self.openai_client: openai.OpenAI = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def detect_content(self, content: str) -> Moderation:
        """
        Detects the content type of the given text using OpenAI's content detection API.

        Args:
            content (str): The text content to be analyzed.

        Returns:
            list[str]: A list of detected content types.
        """
        # return early if content is empty or None, may want to change this to require some content
        # but for now, we want to avoid sending empty content to the API

        def _build_moderation_response_from_detected_types(d_types: Set[str]) -> Moderation:
            detected_map: Dict[str, bool] = {
                k: (k in d_types) for k in self.CATEGORY_PATTERNS
            }
            return Moderation(
                flagged=bool(d_types),
                categories=detected_map,
                category_scores={k: float(v) for k, v in detected_map.items()},
                category_applied_input_types={k: ["text"] if v else [] for k, v in detected_map.items()},
            )

        if not content:
            return _build_moderation_response_from_detected_types(set())

        detected_types = self._detect_by_keywords(content)
        logger.info(f"Internal detection - content={content}, detected_types={detected_types}")

        # if regex catches something, return early to save on api call
        if detected_types:
            return _build_moderation_response_from_detected_types(detected_types)

        response = self.openai_client.moderations.create(
            model="omni-moderation-latest",
            input=content,
        )

        return response.results[0]

    def _detect_by_keywords(self, content: str) -> Set[str]:
        """
        Detects content types based on predefined keywords.

        Args:
            content (str): The text content to be analyzed.

        Returns:
            Set[str]: A list of detected content types.
        """
        detected_types: Set[str] = set()

        for category, patterns in self.CATEGORY_PATTERNS.items():
            for pattern in patterns:
                if pattern.search(content):
                    detected_types.add(category)
                    break

        return detected_types


# TODO: replace with DI/singleton
default_content_detection_service = ContentDetectionService()
