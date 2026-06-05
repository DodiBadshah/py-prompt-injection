from __future__ import annotations

import datetime
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader

from llm_probe.schemas.result import Result
from llm_probe.core.logging import logger

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_TEMPLATE_NAME = "report.html.j2"


def render_html(results: List[Result], model: str, output_path: Path) -> Path:
    """Render a list of Result objects to an HTML report file."""

    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATE_DIR)),
        autoescape=True,
    )
    template = env.get_template(_TEMPLATE_NAME)

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    pass_rate = round((passed / total * 100), 1) if total > 0 else 0.0

    rows = [
        {
            "payload_id": r.payload_id,
            "category": r.owasp_category,
            "severity": next((f for f in r.flags if f in ("low", "medium", "high", "critical")), "medium"),
            "passed": r.passed,
            "score": r.score,
            "raw_response": r.response_text or "",
            "flags": r.flags,
        }
        for r in results
    ]

    html = template.render(
        model=model,
        total=total,
        passed=passed,
        failed=failed,
        pass_rate=pass_rate,
        generated_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M (local)"),
        results=rows,
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    logger.info(f"HTML report written to {output_path}")
    return output_path