# tests/test_loader.py
"""Tests for payloads/loader.py."""

import pytest
from llm_probe.payloads.loader import load_all_payloads, load_by_category
from llm_probe.schemas.payload import Payload, OwaspCategory
from llm_probe.core.exceptions import PayloadLoadError


def test_load_all_payloads_returns_list():
    payloads = load_all_payloads()
    assert isinstance(payloads, list)
    assert len(payloads) > 0


def test_load_all_payloads_all_are_payload_objects():
    payloads = load_all_payloads()
    for p in payloads:
        assert isinstance(p, Payload)


def test_load_all_payloads_ids_are_unique():
    payloads = load_all_payloads()
    ids = [p.id for p in payloads]
    assert len(ids) == len(set(ids))


def test_load_all_payloads_covers_all_categories():
    payloads = load_all_payloads()
    categories = {p.owasp_category for p in payloads}
    assert OwaspCategory.LLM01 in categories
    assert OwaspCategory.LLM02 in categories
    assert OwaspCategory.LLM06 in categories
    assert OwaspCategory.LLM08 in categories


def test_load_by_category_llm01():
    payloads = load_by_category("LLM01")
    assert len(payloads) > 0
    for p in payloads:
        assert p.owasp_category == OwaspCategory.LLM01


def test_load_by_category_llm08():
    payloads = load_by_category("LLM08")
    assert len(payloads) > 0
    for p in payloads:
        assert p.owasp_category == OwaspCategory.LLM08


def test_load_by_category_unknown_returns_empty():
    payloads = load_by_category("LLM99")
    assert payloads == []


def test_load_all_payloads_no_empty_prompt_text():
    payloads = load_all_payloads()
    for p in payloads:
        assert p.prompt_text.strip() != ""


def test_load_all_payloads_no_empty_expected_behavior():
    payloads = load_all_payloads()
    for p in payloads:
        assert p.expected_behavior.strip() != ""