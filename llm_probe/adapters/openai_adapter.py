import time
import openai
from llm_probe.adapters.base import BaseAdapter
from llm_probe.core.config import settings
from llm_probe.core.logging import logger
from llm_probe.core.exceptions import AdapterError
from llm_probe.schemas.payload import Payload
from llm_probe.schemas.result import Result


class OpenAIAdapter(BaseAdapter):
    """Adapter for OpenAI chat completion models."""

    def __init__(self, model: str | None = None, timeout: int | None = None) -> None:
        super().__init__(
            model=model or settings.default_model,
            timeout=timeout or settings.request_timeout_seconds,
        )
        self._client = openai.OpenAI(
            api_key=settings.openai_api_key,
            timeout=self.timeout,
        )

    def send(self, payload: Payload) -> Result:
        logger.debug(f"OpenAI send | model={self.model} | payload_id={payload.id}")
        start = time.monotonic()
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": payload.prompt_text}],
                max_tokens=512,
            )
            elapsed_ms = round((time.monotonic() - start) * 1000)
            raw_response = response.choices[0].message.content or ""
            return Result(
                payload_id=payload.id,
                owasp_category=payload.owasp_category,
                provider="openai",
                model=self.model,
                prompt_text=payload.text,
                response_text=raw_response,
                score=0.0,
                passed=False,
                latency_ms=elapsed_ms,
            )
        except openai.OpenAIError as exc:
            raise AdapterError(f"OpenAI API error: {exc}") from exc