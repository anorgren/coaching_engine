import logging

from openai import OpenAI
from openai.types.beta import Assistant

from ..config import settings
from ..dto import Coach, DailyMetric, UserProfile

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client for OpenAI API."""

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    def get_assistant(self, assistant_id: str) -> Assistant:
        """Get an assistant by ID."""
        assistant = self.client.beta.assistants.retrieve(assistant_id)
        return assistant

    def get_all_assistants(self) -> list[Assistant]:
        """Get all assistants."""
        assistants = self.client.beta.assistants.list()

        return assistants

    def create_assistant(self, coach: Coach) -> Assistant:
        """Create an assistant."""
        default_tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_recommendation",
                    "description": "Get a health related recommendation for the user.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_profile": {
                                "type": "object",
                                "description": "Information about the user."
                            },
                            "daily_metrics": {
                                "type": "object",
                                "description": "Health related metrics for the user."
                            }
                        },
                        "required": ["user_profile", "daily_metrics"]
                    }
                }
            },
        ]
        assistant = self.client.beta.assistants.create(
            model=coach.model,
            instructions=coach.instructions,
            name=coach.name,
            metadata=coach.metadata,
            tools=default_tools,
        )
        return assistant

    def update_assistant(
        self,
        coach: Coach,
    ) -> Assistant:
        """Update an assistant."""
        assistant = self.client.beta.assistants.update(
            assistant_id=coach.id,
            model=coach.model,
            instructions=coach.instructions,
            name=coach.name,
            metadata=coach.metadata,
        )

        return assistant

    def create_recommendation(self, coach_id: str, profile: UserProfile, metrics: DailyMetric):
        """Create a recommendation using the assistant."""
        message_content = {
            "user_profile": profile,
            "daily_metrics": metrics,
        }

        thread = self.client.beta.threads.create()
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=str(message_content)
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=coach_id,
        )

        logger.info(f"Run status: {run.status}")
        print(f"Run status: {run.status} - run={run}")

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            print(messages)
            return messages
        elif run.status == 'requires_action':
            self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=run.required_action.submit_tool_outputs
            )

        return None
