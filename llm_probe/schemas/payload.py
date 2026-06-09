# llm_probe/schemas/payload.py
"""
Pydantic model for a single test payload.
Every entry in payloads/catalog/*.yaml is validated against this schema
when loaded. If a field is missing or has the wrong type, PayloadLoadError
is raised before any API call is made.
"""
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field


class OwaspCategory(str, Enum):
    LLM01 = "LLM01"  # Prompt Injection
    LLM02 = "LLM02"  # Insecure Output Handling
    LLM06 = "LLM06"  # Sensitive Information Disclosure
    LLM08 = "LLM08"  # Excessive Agency


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# Valid expected_behavior values recognised by the scoring engine.
# "fallback" and any unrecognised value routes to generic heuristic scoring.
ExpectedBehavior = Literal[
    "refusal",
    "no_exfiltration",
    "no_code_execution",
    "no_sensitive_data",
    "no_agency",
]


class Payload(BaseModel):
    """A single prompt injection test payload."""

    id: str = Field(
        ...,
        description="Unique identifier, e.g. llm01-001",
        pattern=r"^llm0[0-9]+-[0-9]{3}$",
    )
    owasp_category: OwaspCategory = Field(
        ...,
        description="OWASP LLM Top 10 category this payload targets.",
    )
    severity: Severity = Field(
        ...,
        description="Risk severity if the model fails this payload.",
    )
    description: str = Field(
        ...,
        description="Human-readable explanation of what this payload tests.",
        min_length=10,
    )
    prompt_text: str = Field(
        ...,
        description="The exact string sent to the LLM under test.",
        min_length=1,
    )
    expected_behavior: ExpectedBehavior = Field(
        ...,
        description=(
            "Machine-readable scoring directive. Must be one of: "
            "refusal, no_exfiltration, no_code_execution, "
            "no_sensitive_data, no_agency."
        ),
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Optional tags for filtering, e.g. ['jailbreak', 'indirect'].",
    )

    model_config = {"frozen": True}