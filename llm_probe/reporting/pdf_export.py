from __future__ import annotations

from pathlib import Path

from loguru import logger


def export_pdf(html_path: Path, pdf_path: Path) -> Path:
    """Convert an HTML report file to PDF using weasyprint."""
    try:
        from weasyprint import HTML
    except ImportError as e:
        raise ImportError(
            "weasyprint is not installed. Run: pip install weasyprint"
        ) from e

    html_path = Path(html_path)
    pdf_path = Path(pdf_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(filename=str(html_path)).write_pdf(str(pdf_path))
    logger.info(f"PDF report written to {pdf_path}")
    return pdf_path