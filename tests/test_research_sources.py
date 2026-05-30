from __future__ import annotations

import pytest

from deep_research_agent.tools import (
    build_source_ledger,
    classify_source,
    create_task_packet,
    prepare_aiq_research_request,
    record_source,
    slugify_topic,
)


def test_create_task_packet_lists_required_artifacts():
    packet = create_task_packet("long-running research agents")

    assert packet["topic"] == "long-running research agents"
    assert "llm-wiki/wiki/research-briefs/<topic>.md" in packet["required_artifacts"]
    assert any("source ID" in rule for rule in packet["review_rules"])


def test_record_source_has_stable_source_id():
    first = record_source("NVIDIA Agent Skills", "https://github.com/NVIDIA/skills")
    second = record_source("NVIDIA Agent Skills", "https://github.com/NVIDIA/skills")

    assert first["source_id"] == second["source_id"]
    assert first["source_id"].startswith("SRC-")


def test_record_source_rejects_non_http_urls():
    with pytest.raises(ValueError, match="http or https"):
        record_source("Local note", "file:///tmp/note.md")


def test_classify_source_marks_github_as_primary():
    result = classify_source("repo", "https://github.com/NVIDIA/skills")

    assert result["review_weight"] == "primary"


def test_build_source_ledger_outputs_markdown_table():
    source = record_source(
        "Deep Agents docs",
        "https://docs.langchain.com/oss/python/deepagents/subagents",
        source_type="official docs",
    )
    ledger = build_source_ledger("deep agents", [source])

    assert ledger["path"] == "llm-wiki/raw/deep_agents_source_ledger.md"
    assert "| Source ID | Title | Type | Retrieved | Notes |" in ledger["markdown"]
    assert source["source_id"] in ledger["markdown"]


def test_slugify_topic_creates_stable_artifact_name():
    assert slugify_topic("Long-running AI research agents") == "long_running_ai_research_agents"
    assert slugify_topic("  ") == "research_topic"


def test_prepare_aiq_request_names_skill_contract(monkeypatch):
    monkeypatch.setenv("AIQ_SERVER_URL", "http://localhost:8000")

    request = prepare_aiq_research_request(
        "What does AI-Q add to a research harness?",
        source_ids=["SRC-12345678"],
    )

    assert request["expected_skill"] == "aiq-research"
    assert request["aiq_server_url"] == "http://localhost:8000"
    assert "poll if a job ID is returned" in request["expected_flow"]
