from __future__ import annotations
import mlflow
from typing import List
from llm_probe.core.logging import logger
from llm_probe.core.exceptions import AdapterError, ScoringError
from llm_probe.schemas.payload import Payload
from llm_probe.schemas.result import Result
from llm_probe.adapters.anthropic_adapter import AnthropicAdapter
from llm_probe.adapters.openai_adapter import OpenAIAdapter
from llm_probe.scoring.engine import score

ADAPTER_MAP = {
    "anthropic": AnthropicAdapter,
    "openai": OpenAIAdapter,
}

class Runner:
    """
    Orchestrates the full probe pipeline:
    load payloads -> send to LLM -> score response -> log to MLflow.
    """

    def __init__(self, adapter_name: str, experiment_name: str = "py-prompt-injection"):
        if adapter_name not in ADAPTER_MAP:
            raise ValueError(f"Unknown adapter: {adapter_name}. Choose from {list(ADAPTER_MAP)}")
        self.adapter = ADAPTER_MAP[adapter_name]()
        self.experiment_name = experiment_name
        logger.info(f"Runner initialised | adapter={adapter_name}")

    def run(self, payloads: List[Payload]) -> List[Result]:
        mlflow.set_experiment(self.experiment_name)
        results: List[Result] = []
        with mlflow.start_run():
            mlflow.log_param("adapter", self.adapter.__class__.__name__)
            mlflow.log_param("payload_count", len(payloads))
            for payload in payloads:
                logger.info(f"Probing | id={payload.id} | category={payload.owasp_category}")
                try:
                    result = self.adapter.send(payload)
                except AdapterError as e:
                    logger.error(f"Adapter error for {payload.id}: {e}")
                    continue
                try:
                    result = score(result, payload)
                except ScoringError as e:
                    logger.error(f"Scoring error for {payload.id}: {e}")
                    continue
                results.append(result)
                mlflow.log_metric("injection_detected",
                                  int("INJECTION_COMPLIANCE" in result.flags),
                                  step=len(results))
                mlflow.log_metric("refusal_detected",
                                  int("REFUSAL_DETECTED" in result.flags),
                                  step=len(results))
            mlflow.log_metric("total_results", len(results))
            logger.info(f"Run complete | total={len(results)}")
        return results