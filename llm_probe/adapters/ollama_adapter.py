import httpx
from llm_probe.schemas.payload import Payload
from llm_probe.schemas.result import Result
from llm_probe.adapters.base import BaseAdapter
from datetime import datetime, timezone


class OllamaAdapter(BaseAdapter):
    def __init__(self, model: str = "phi3:mini", base_url: str = "http://172.31.192.1:11434"):
        self.model = model
        self.base_url = base_url

    def send(self, payload: Payload) -> Result:
        prompt = payload.prompt_text
        started = datetime.now(timezone.utc)

        try:
            response = httpx.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
                timeout=120.0,
            )
            response.raise_for_status()
            data = response.json()
            reply = data["message"]["content"]
            error = None
        except Exception as e:
            reply = ""
            error = str(e)

        ended = datetime.now(timezone.utc)
        latency = int((ended - started).total_seconds() * 1000)

        return Result(
            payload_id=payload.id,
            owasp_category=payload.owasp_category,
            provider="ollama",
            model=self.model,
            prompt_text=prompt,
            response_text=reply,
            score=0.0,
            passed=True,
            latency_ms=latency,
            flags=[],
        )