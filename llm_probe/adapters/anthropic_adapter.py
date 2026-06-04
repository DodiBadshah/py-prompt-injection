import time
import anthropic
from llm_probe.adapters.base import BaseAdapter
from llm_probe.core.config import settings
from llm_probe.core.logging import logger
from llm_probe.core.exceptions import AdapterError
from llm_probe.schemas.payload import Payload
from llm_probe.schemas.result import Result


class AnthropicAdapter(BaseAdapter):
    """Adapter for Anthropic Claude models."""

    def __init__(self, model: str | None = None, timeout: int | None = None) -> None:
        super().__init__(
            model=model or settings.default_model,
            timeout=timeout or settings.request_timeout_seconds,
        )
        self._client = anthropic.Anthropic(
            api_key=settings.anthropic_api_key,
            timeout=self.timeout,
        )

    def send(self, payload: Payload) -> Result:
        logger.debug(f"Anthropic send | model={self.model} | payload_id={payload.id}")
        start = time.monotonic()
        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": payload.prompt_text}],
            )
            elapsed_ms = round((time.monotonic() - start) * 1000)
            raw_response = response.content[0].text if response.content else ""
            return Result(
                payload_id=payload.id,
                owasp_category=payload.owasp_category,
                provider="anthropic",
                model=self.model,
                prompt_text=payload.prompt_text,
                response_text=raw_response,
                score=0.0,
                passed=False,
                latency_ms=elapsed_ms,
            )
        except anthropic.APIError as exc:
            raise AdapterError(f"Anthropic API error: {exc}") from exc