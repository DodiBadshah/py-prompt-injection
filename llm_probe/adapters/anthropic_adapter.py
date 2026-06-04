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
            model=model or settings.anthropic_default_model,
            timeout=timeout or settings.request_timeout,
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
                messages=[{"role": "user", "content": payload.text}],
            )
            elapsed = round(time.monotonic() - start, 3)
            raw_response = response.content[0].text if response.content else ""
            return Result(
                payload_id=payload.id,
                category=payload.category,
                model=self.model,
                provider="anthropic",
                prompt=payload.text,
                raw_response=raw_response,
                latency_seconds=elapsed,
            )
        except anthropic.APIError as exc:
            raise AdapterError(f"Anthropic API error: {exc}") from exc