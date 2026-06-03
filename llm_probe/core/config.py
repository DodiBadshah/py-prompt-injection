# llm_probe/core/config.py
"""
Central configuration for py-prompt-injection.

Reads all settings from the .env file using pydantic-settings BaseSettings.
Every module that needs a config value imports the `settings` object from here.
Never read os.environ directly anywhere else in the codebase.

Usage:
    from llm_probe.core.config import settings

    api_key = settings.anthropic_api_key
    timeout = settings.request_timeout_seconds
"""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from llm_probe.core.exceptions import ProbeConfigError


class Settings(BaseSettings):
    """
    All runtime configuration for py-prompt-injection.

    Values are loaded from the .env file in the project root.
    See .env.example for the full list of supported variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- API Keys ---------------------------------------------------
    anthropic_api_key: str = Field(
        default="",
        description="Anthropic API key. Required when provider is anthropic.",
    )
    openai_api_key: str = Field(
        default="",
        description="OpenAI API key. Required when provider is openai.",
    )

    # --- Model Selection --------------------------------------------
    default_model: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="Model used when --model flag is not passed to CLI.",
    )
    default_provider: str = Field(
        default="anthropic",
        description="Provider used when --provider flag is not passed to CLI.",
    )

    # --- Test Run Behaviour -----------------------------------------
    max_payloads_per_run: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum payloads per session. Safety cap.",
    )
    request_delay_seconds: float = Field(
        default=0.5,
        ge=0.0,
        description="Seconds to wait between API calls. Rate limit buffer.",
    )
    request_timeout_seconds: int = Field(
        default=30,
        ge=5,
        le=120,
        description="Per-request timeout in seconds.",
    )

    # --- Scoring ----------------------------------------------------
    score_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum score to flag a result as a finding.",
    )

    # --- Reporting --------------------------------------------------
    report_output_dir: Path = Field(
        default=Path("reports/"),
        description="Directory for generated HTML and PDF reports.",
    )

    # --- MLflow -----------------------------------------------------
    mlflow_tracking_uri: str = Field(
        default="mlruns/",
        description="MLflow tracking URI. Local by default.",
    )
    mlflow_experiment_name: str = Field(
        default="py-prompt-injection",
        description="MLflow experiment label.",
    )

    # --- Validators -------------------------------------------------
    @field_validator("default_provider")
    @classmethod
    def provider_must_be_supported(cls, v: str) -> str:
        supported = {"anthropic", "openai"}
        if v.lower() not in supported:
            raise ValueError(f"default_provider must be one of {supported}, got '{v}'")
        return v.lower()

    @field_validator("report_output_dir")
    @classmethod
    def ensure_report_dir_exists(cls, v: Path) -> Path:
        v.mkdir(parents=True, exist_ok=True)
        return v


def load_settings() -> Settings:
    """
    Load and return the validated Settings object.

    Wraps pydantic validation errors in ProbeConfigError so the CLI
    can catch a single exception type for all config problems.

    Returns:
        Settings: Validated configuration object.

    Raises:
        ProbeConfigError: If any required setting is missing or invalid.
    """
    try:
        return Settings()
    except Exception as exc:
        raise ProbeConfigError(
            message="Configuration failed to load. Check your .env file.",
            detail=str(exc),
        ) from exc


# Module-level singleton -- import this everywhere.
settings = load_settings()