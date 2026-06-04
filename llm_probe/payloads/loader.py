"""
llm_probe/payloads/loader.py

Reads all YAML payload catalogs from the catalog/ directory,
validates each entry against the Payload schema, and returns
a list of validated Payload objects.

Raises PayloadLoadError on any missing file or validation failure.
"""

from pathlib import Path

import yaml
from pydantic import ValidationError

from llm_probe.core.exceptions import PayloadLoadError
from llm_probe.core.logging import logger
from llm_probe.schemas.payload import Payload

CATALOG_DIR = Path(__file__).parent / "catalog"

CATALOG_FILES = [
    "llm01_prompt_injection.yaml",
    "llm02_insecure_output.yaml",
    "llm06_sensitive_disclosure.yaml",
    "llm08_excessive_agency.yaml",
]


def load_all_payloads() -> list[Payload]:
    """
    Load and validate all payloads from the catalog directory.

    Returns a list of validated Payload objects.
    Raises PayloadLoadError if any file is missing or any entry
    fails Pydantic validation.
    """
    all_payloads: list[Payload] = []

    for filename in CATALOG_FILES:
        filepath = CATALOG_DIR / filename

        if not filepath.exists():
            raise PayloadLoadError(
                f"Catalog file not found: {filepath}"
            )

        logger.info(f"Loading catalog: {filename}")

        with filepath.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        entries = raw.get("payloads", [])

        for entry in entries:
            try:
                payload = Payload(**entry)
                all_payloads.append(payload)
            except ValidationError as exc:
                raise PayloadLoadError(
                    f"Validation failed in {filename} for entry "
                    f"{entry.get('id', 'unknown')}: {exc}"
                ) from exc

        logger.info(f"Loaded {len(entries)} payloads from {filename}")

    logger.info(f"Total payloads loaded: {len(all_payloads)}")
    return all_payloads


def load_by_category(owasp_category: str) -> list[Payload]:
    """
    Load all payloads then filter by OWASP category.

    Example: load_by_category("LLM01")
    """
    all_payloads = load_all_payloads()
    filtered = [p for p in all_payloads if p.owasp_category == owasp_category]
    logger.info(
        f"Filtered to {len(filtered)} payloads for category {owasp_category}"
    )
    return filtered