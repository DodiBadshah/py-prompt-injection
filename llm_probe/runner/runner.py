from __future__ import annotations
import mlflow
from typing import List
from llm_probe.core.logging import logger
from llm_probe.core.exceptions import AdapterError, ScoringError
from llm_probe.schemas.payload import Payload
from llm_probe.schemas.result import Result
from llm_probe.adapters.anthropic_adapter import AnthropicAdapter
from llm_probe.adapters.openai_adapter import OpenAIAdapter
from llm_probe.adapters.ollama_adapter import OllamaAdapter
from llm_probe.scoring.engine import score

ADAPTER_MAP = {
    "anthropic": AnthropicAdapter,
    "openai": OpenAIAdapter,
    "ollama": OllamaAdapter,
}


class Runner:
    """
    Orchestrates the full probe pipeline:
    load payloads -> send to LLM -> score response -> log to MLflow.

    When runs > 1, each payload is executed runs times and scores are
    averaged. Score variance and verdict stability are logged to MLflow
    to surface instability documented in FIND-G2-07.
    """

    def __init__(self, adapter_name: str, experiment_name: str = "py-prompt-injection"):
        if adapter_name not in ADAPTER_MAP:
            raise ValueError(f"Unknown adapter: {adapter_name}. Choose from {list(ADAPTER_MAP)}")
        self.adapter = ADAPTER_MAP[adapter_name]()
        self.experiment_name = experiment_name
        logger.info(f"Runner initialised | adapter={adapter_name}")

    def run(self, payloads: List[Payload], runs: int = 1) -> List[Result]:
        """
        Run all payloads against the adapter.

        Args:
            payloads: List of Payload objects to evaluate.
            runs: Number of times to run each payload. When > 1, scores
                  are averaged and variance is logged (--multi-run mode).
        """
        mlflow.set_experiment(self.experiment_name)
        results: List[Result] = []

        with mlflow.start_run():
            mlflow.log_param("adapter", self.adapter.__class__.__name__)
            mlflow.log_param("payload_count", len(payloads))
            mlflow.log_param("runs_per_payload", runs)

            for payload in payloads:
                logger.info(f"Probing | id={payload.id} | category={payload.owasp_category} | runs={runs}")

                if runs == 1:
                    result = self._run_single(payload)
                    if result is None:
                        continue
                else:
                    result = self._run_multi(payload, runs)
                    if result is None:
                        continue

                results.append(result)

                # MLflow per-payload metrics
                mlflow.log_metric(
                    "injection_detected",
                    int("INJECTION_COMPLIANCE" in result.flags),
                    step=len(results),
                )
                mlflow.log_metric(
                    "refusal_detected",
                    int("REFUSAL_DETECTED" in result.flags),
                    step=len(results),
                )

                # Multi-run variance metrics
                if result.score_variance is not None:
                    mlflow.log_metric(
                        "score_variance",
                        result.score_variance,
                        step=len(results),
                    )
                    mlflow.log_metric(
                        "verdict_stable",
                        int(result.verdict_stable),
                        step=len(results),
                    )
                    if not result.verdict_stable:
                        logger.warning(
                            f"Unstable verdict | id={payload.id} | "
                            f"scores ranged {result.score_min:.2f}-{result.score_max:.2f} | "
                            f"variance={result.score_variance:.4f}"
                        )

            mlflow.log_metric("total_results", len(results))

            if runs > 1:
                unstable = sum(1 for r in results if r.verdict_stable is False)
                mlflow.log_metric("unstable_verdicts", unstable)
                logger.info(f"Multi-run complete | total={len(results)} | unstable_verdicts={unstable}")
            else:
                logger.info(f"Run complete | total={len(results)}")

        return results

    def _run_single(self, payload: Payload):
        """Execute a single payload run. Returns Result or None on error."""
        try:
            result = self.adapter.send(payload)
        except AdapterError as e:
            logger.error(f"Adapter error for {payload.id}: {e}")
            return None
        try:
            result = score(result, payload)
        except ScoringError as e:
            logger.error(f"Scoring error for {payload.id}: {e}")
            return None
        return result

    def _run_multi(self, payload: Payload, runs: int):
        """
        Execute a payload runs times, average scores, compute variance.
        Returns a Result with multi-run fields populated, or None if all runs fail.
        """
        scored_results = []

        for i in range(runs):
            logger.debug(f"Run {i + 1}/{runs} | id={payload.id}")
            try:
                result = self.adapter.send(payload)
                result = score(result, payload)
                scored_results.append(result)
            except (AdapterError, ScoringError) as e:
                logger.warning(f"Run {i + 1} failed for {payload.id}: {e}")
                continue

        if not scored_results:
            logger.error(f"All {runs} runs failed for {payload.id}")
            return None

        scores = [r.score for r in scored_results]
        passed_flags = [r.passed for r in scored_results]
        latencies = [r.latency_ms for r in scored_results]

        mean_score = sum(scores) / len(scores)
        mean_latency = int(sum(latencies) / len(latencies))
        score_variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        score_min = min(scores)
        score_max = max(scores)
        verdict_stable = len(set(passed_flags)) == 1

        # Derive averaged passed from majority vote on individual run verdicts.
        # In this scoring system score=0.0 means FAIL (not safe), so comparing
        # mean_score against a threshold would invert the result.
        # A payload passes only if it passed in the majority of runs.
        passed_count = sum(1 for p in passed_flags if p)
        mean_passed = passed_count > (len(scored_results) / 2)

        # Use last run's response text and flags as representative
        last = scored_results[-1]

        # Build averaged result using model_copy to unfreeze for construction
        averaged = Result(
            payload_id=last.payload_id,
            owasp_category=last.owasp_category,
            provider=last.provider,
            model=last.model,
            prompt_text=last.prompt_text,
            response_text=last.response_text,
            score=round(mean_score, 4),
            passed=mean_passed,
            latency_ms=mean_latency,
            flags=last.flags,
            timestamp=last.timestamp,
            run_count=len(scored_results),
            score_variance=round(score_variance, 6),
            score_min=round(score_min, 4),
            score_max=round(score_max, 4),
            verdict_stable=verdict_stable,
        )

        logger.info(
            f"Multi-run result | id={payload.id} | "
            f"mean={mean_score:.3f} | variance={score_variance:.4f} | "
            f"stable={verdict_stable} | runs_completed={len(scored_results)}/{runs}"
        )

        return averaged
