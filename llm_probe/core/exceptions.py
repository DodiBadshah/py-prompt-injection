# llm_probe/core/exceptions.py
"""
Custom exception hierarchy for py-prompt-injection.

All project exceptions inherit from ProbeBaseError so the CLI can catch
everything in one place while still allowing granular handling per layer.
"""


class ProbeBaseError(Exception):
    """Base class for all py-prompt-injection exceptions."""

    def __init__(self, message: str, detail: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail

    def __str__(self) -> str:
        if self.detail:
            return f"{self.message} | detail: {self.detail}"
        return self.message


class ProbeConfigError(ProbeBaseError):
    """
    Raised when configuration is missing, invalid, or cannot be loaded.

    Examples:
        - ANTHROPIC_API_KEY not set in .env
        - SCORE_THRESHOLD outside 0.0-1.0 range
        - .env file not found
    """


class AdapterError(ProbeBaseError):
    """
    Raised when an API adapter fails to complete a request.

    Examples:
        - Authentication failure (401)
        - Rate limit hit (429)
        - Network timeout
        - Unexpected response format
    """


class PayloadLoadError(ProbeBaseError):
    """
    Raised when a payload YAML file cannot be loaded or fails validation.

    Examples:
        - YAML syntax error in catalog file
        - Required field missing from payload definition
        - Unknown OWASP category tag
    """


class ScoringError(ProbeBaseError):
    """
    Raised when the scoring engine cannot process a model response.

    Examples:
        - Response object missing expected fields
        - Heuristic pattern compilation failure
    """