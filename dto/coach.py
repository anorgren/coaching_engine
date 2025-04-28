from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import enum


class AssistantTool(str, enum.Enum):
    """A function tool."""
    FUNCTION = "function"
    FILE_SEARCH = "file_search"
    CODE_INTERPRETER = "code_interpreter"


class GPTModel(str, enum.Enum):
    """Allowable GPT models."""
    GPT_3_5_TURBO = "gpt-3.5-turbo-1106"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4_0_MINI = "gpt-4o-mini"


class Metadata(BaseModel):
    """Internal metadata for the assistant."""
    user_id: Optional[str]
    internal_coach_id: Optional[str]


class Coach(BaseModel):
    """A class representing a coach assistant."""
    id: Optional[str] = None
    """The identifier, which can be referenced in API endpoints."""

    created_at: Optional[int] = None
    """The Unix timestamp (in seconds) for when the assistant was created."""

    description: Optional[str] = None
    """The description of the assistant. The maximum length is 512 characters."""

    instructions: Optional[str] = None
    """The system instructions that the assistant uses.

    The maximum length is 256,000 characters.
    """

    metadata: Optional[Metadata] = None
    """Set of 16 key-value pairs that can be attached to an object.

    This can be useful for storing additional information about the object in a
    structured format, and querying for objects via API or the dashboard.

    Keys are strings with a maximum length of 64 characters. Values are strings with
    a maximum length of 512 characters.
    """

    model: Optional[str] = None
    """ID of the model to use.

    You can use the
    [List models](https://platform.openai.com/docs/api-reference/models/list) API to
    see all of your available models, or see our
    [Model overview](https://platform.openai.com/docs/models) for descriptions of
    them.
    """

    name: Optional[str] = None
    """The name of the assistant. The maximum length is 256 characters."""

    tools: List[AssistantTool] = []
    """A list of tool enabled on the assistant.

    There can be a maximum of 128 tools per assistant. Tools can be of types
    `code_interpreter`, `file_search`, or `function`.
    """

    # response_format: Optional[AssistantResponseFormatOption] = None
    # """Specifies the format that the model must output.
    #
    # Compatible with [GPT-4o](https://platform.openai.com/docs/models#gpt-4o),
    # [GPT-4 Turbo](https://platform.openai.com/docs/models#gpt-4-turbo-and-gpt-4),
    # and all GPT-3.5 Turbo models since `gpt-3.5-turbo-1106`.
    #
    # Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured
    # Outputs which ensures the model will match your supplied JSON schema. Learn more
    # in the
    # [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
    #
    # Setting to `{ "type": "json_object" }` enables JSON mode, which ensures the
    # message the model generates is valid JSON.
    #
    # **Important:** when using JSON mode, you **must** also instruct the model to
    # produce JSON yourself via a system or user message. Without this, the model may
    # generate an unending stream of whitespace until the generation reaches the token
    # limit, resulting in a long-running and seemingly "stuck" request. Also note that
    # the message content may be partially cut off if `finish_reason="length"`, which
    # indicates the generation exceeded `max_tokens` or the conversation exceeded the
    # max context length.
    # """

    temperature: Optional[float] = None
    """What sampling temperature to use, between 0 and 2.

    Higher values like 0.8 will make the output more random, while lower values like
    0.2 will make it more focused and deterministic.
    """

    top_p: Optional[float] = None
    """
    An alternative to sampling with temperature, called nucleus sampling, where the
    model considers the results of the tokens with top_p probability mass. So 0.1
    means only the tokens comprising the top 10% probability mass are considered.

    We generally recommend altering this or temperature but not both.
    """

    class Config:
        from_attributes = True
