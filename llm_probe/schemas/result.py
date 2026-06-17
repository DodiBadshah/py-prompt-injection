# llm_probe/schemas/result.py
"""
Pydantic model for a single test result.

Produced by the scoring engine after each LLM response is evaluated.
The reporter consumes a list of these to build HTML and PDF output.
"""

from datetime import datetime, timezone
from typing import Optional

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
        description="Raw response returned by the LLM. In multi-run mode, the last run response.",
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Heuristic risk score. 0.0 = safe, 1.0 = fully compromised. In multi-run mode, the mean across all runs.",
    )
    passed: bool = Field(
        ...,
        description="True if score is below the configured SCORE_THRESHOLD.",
    )
    latency_ms: int = Field(
        ...,
        ge=0,
        description="API round-trip time in milliseconds. In multi-run mode, the mean latency.",
    )
    flags: list[str] = Field(
        default_factory=list,
        description="Heuristic flags that fired, e.g. ['refusal_bypass', 'credential_leak'].",
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp set automatically when the result is created.",
    )

    # Multi-run fields: only populated when --multi-run > 1
    run_count: Optional[int] = Field(
        default=None,
        description="Number of runs averaged. None in single-run mode.",
    )
    score_variance: Optional[float] = Field(
        default=None,
        description="Variance of scores across runs. High variance indicates instability (see FIND-G2-07).",
    )
    score_min: Optional[float] = Field(
        default=None,
        description="Minimum score observed across runs.",
    )
    score_max: Optional[float] = Field(
        default=None,
        description="Maximum score observed across runs.",
    )
    verdict_stable: Optional[bool] = Field(
        default=None,
        description="True if passed/failed verdict was identical across all runs. False indicates instability.",
    )

    model_config = {"frozen": True}
