from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Optional
import typer
from loguru import logger
from llm_probe.core.logging import setup_logging
from llm_probe.core.exceptions import ProbeConfigError, AdapterError, PayloadLoadError
from llm_probe.payloads.loader import load_all_payloads, load_by_category
from llm_probe.adapters.openai_adapter import OpenAIAdapter
from llm_probe.adapters.anthropic_adapter import AnthropicAdapter
from llm_probe.adapters.ollama_adapter import OllamaAdapter
from llm_probe.runner.runner import Runner
from llm_probe.reporting.renderer import render_html
from llm_probe.reporting.pdf_export import export_pdf

app = typer.Typer(
    name="llm-probe",
    help="Black-box prompt injection test harness for LLMs.",
    add_completion=False,
)

def _pick_adapter(model: str):
    m = model.lower()
    if m.startswith("gpt") or m.startswith("o1") or m.startswith("o3"):
        return OpenAIAdapter(model=model)
    if m.startswith("claude"):
        return AnthropicAdapter(model=model)
    if m.startswith("phi") or m.startswith("mistral") or m.startswith("llama") or m.startswith("gemma"):
        return OllamaAdapter(model=model)
    raise ProbeConfigError(f"Cannot infer provider from model name {model!r}.")

@app.command()
def run(
    model: str = typer.Option(..., "--model", "-m", help="Model identifier."),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="HTML report path."),
    pdf: bool = typer.Option(False, "--pdf", help="Also export a PDF."),
    owasp: Optional[str] = typer.Option(None, "--owasp", help="Filter by OWASP category e.g. LLM01."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose logging."),
    multi_run: int = typer.Option(
        1,
        "--multi-run",
        "-n",
        min=1,
        max=10,
        help=(
            "Number of times to run each payload. Scores are averaged across runs "
            "and variance is logged to MLflow. Use 3 to address scoring instability "
            "documented in FIND-G2-07. Default: 1 (single run, original behaviour)."
        ),
    ),
) -> None:
    """Run the prompt injection test suite against a model."""
    setup_logging(log_level="DEBUG" if verbose else "INFO")

    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_model = model.replace(":", "-").replace("/", "-")
        run_suffix = f"-x{multi_run}" if multi_run > 1 else ""
        output = Path(f"reports/report-{timestamp}-{safe_model}{run_suffix}.html")

    logger.info(f"Starting llm-probe against model: {model}")
    if multi_run > 1:
        logger.info(f"Multi-run mode: each payload will run {multi_run} times, scores averaged")

    try:
        if owasp:
            tag = owasp.upper()
            payloads = load_by_category(tag)
            if not payloads:
                logger.error(f"No payloads found for OWASP category: {tag}")
                raise typer.Exit(code=1)
            logger.info(f"Filtered to {len(payloads)} payloads for category {tag}")
        else:
            payloads = load_all_payloads()
            logger.info(f"Loaded {len(payloads)} payloads")
    except PayloadLoadError as exc:
        logger.error(f"Failed to load payloads: {exc}")
        raise typer.Exit(code=1)

    try:
        adapter = _pick_adapter(model)
    except ProbeConfigError as exc:
        logger.error(str(exc))
        raise typer.Exit(code=1)

    runner = Runner(
        adapter_name="ollama" if isinstance(adapter, OllamaAdapter) else (
            "anthropic" if model.lower().startswith("claude") else "openai"
        )
    )
    runner.adapter = adapter

    try:
        results = runner.run(payloads=payloads, runs=multi_run)
    except AdapterError as exc:
        logger.error(f"Adapter error during run: {exc}")
        raise typer.Exit(code=1)

    output.parent.mkdir(parents=True, exist_ok=True)
    render_html(results=results, output_path=output, model=model)
    logger.info(f"HTML report written to {output}")

    if pdf:
        pdf_path = output.with_suffix(".pdf")
        export_pdf(html_path=output, pdf_path=pdf_path)
        logger.info(f"PDF report written to {pdf_path}")

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    if multi_run > 1:
        unstable = sum(1 for r in results if r.verdict_stable is False)
        typer.echo(f"Results: {passed}/{total} payloads passed (averaged over {multi_run} runs).")
        if unstable:
            typer.echo(
                f"Warning: {unstable}/{total} payloads had unstable verdicts across runs "
                f"(passed in some runs, failed in others). See MLflow for variance details."
            )
    else:
        typer.echo(f"Results: {passed}/{total} payloads passed.")

    if passed < total:
        raise typer.Exit(code=2)


def main() -> None:
    app()

if __name__ == "__main__":
    main()
