# llm_probe/schemas/result.py
"""
Pydantic model for a single test result.

Produced by the scoring engine after each LLM response is evaluated.
The reporter consumes a list of these to build HTML and PDF output.
"""

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from llm_probe.schemas.payload import OwaspCategory


class Result(BaseModel):
    """A single scored test result."""

    payload_id: str = Field(
        ...,
        description="The id of the Payload that produced this result.",
    )
    owasp_category: OwaspCategory = Field(
        ...,
        description="OWASP category copied from the payload for easy report grouping.",
    )
    provider: str = Field(
        ...,
        description="API provider used, e.g. 'anthropic' or 'openai'.",
    )
    model: str = Field(
        ...,
        description="Exact model string used, e.g. 'claude-sonnet-4-6'.",
    )
    prompt_text: str = Field(
        ...,
        description="Snapshot of the prompt sent. Stored here so the report is self-contained.",
    )
    response_text: str = Field(
        ...,
        description="Raw response returned by the LLM.",
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Heuristic risk score. 0.0 = safe, 1.0 = fully compromised.",
    )
    passed: bool = Field(
        ...,
        description="True if score is below the configured SCORE_THRESHOLD.",
    )
    latency_ms: int = Field(
        ...,
        ge=0,
        description="API round-trip time in milliseconds.",
    )
    flags: list[str] = Field(
        default_factory=list,
        description="Heuristic flags that fired, e.g. ['refusal_bypass', 'credential_leak'].",
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp set automatically when the result is created.",
    )

    model_config = {"frozen": True}