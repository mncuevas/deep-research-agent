"""Deterministic research-source helpers for the workshop harness."""

from __future__ import annotations

import hashlib
import os
import re
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse


def _stable_source_id(title: str, url: str) -> str:
    digest = hashlib.sha1(f"{title.strip()}|{url.strip()}".encode()).hexdigest()
    return f"SRC-{digest[:8].upper()}"


def slugify_topic(topic: str) -> str:
    """Return a filesystem-safe slug for workshop artifact paths."""

    slug = re.sub(r"[^a-z0-9]+", "_", topic.lower()).strip("_")
    return slug or "research_topic"


def create_task_packet(
    topic: str,
    scope: str = "public sources only",
    deliverable: str = "research brief",
) -> dict[str, Any]:
    """Create a structured research packet for a long-running agent run."""

    if not topic.strip():
        raise ValueError("topic is required")
    return {
        "topic": topic.strip(),
        "scope": scope.strip() or "public sources only",
        "deliverable": deliverable.strip() or "research brief",
        "required_artifacts": [
            "llm-wiki/wiki/research-briefs/<topic>.md",
            "llm-wiki/raw/<topic>_source_ledger.md",
            "llm-wiki/raw/<topic>_open_questions.md",
            "llm-wiki/raw/<topic>_run_log.md",
        ],
        "review_rules": [
            "Every important claim needs a source ID.",
            "Unresolved questions stay visible.",
            "Unavailable skills and failed tool calls are recorded.",
            "Draft reports remain draft until reviewed.",
        ],
    }


def record_source(
    title: str,
    url: str,
    source_type: str = "web",
    notes: str = "",
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    """Return a normalized source record for the source ledger."""

    title = title.strip()
    url = url.strip()
    if not title:
        raise ValueError("title is required")
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("url must be an http or https URL")

    return {
        "source_id": _stable_source_id(title, url),
        "title": title,
        "url": url,
        "source_type": source_type.strip() or "web",
        "notes": notes.strip(),
        "retrieved_at": retrieved_at or datetime.now(UTC).date().isoformat(),
    }


def classify_source(source_type: str, url: str) -> dict[str, str]:
    """Classify a source so reviewers can see how much weight it should carry."""

    normalized_type = source_type.lower().strip()
    host = urlparse(url).netloc.lower()
    if "docs." in host or "github.com" in host or "arxiv.org" in host:
        default_weight = "primary"
    elif normalized_type in {"official docs", "spec", "repo", "release notes"}:
        default_weight = "primary"
    elif normalized_type in {"blog", "analysis", "article"}:
        default_weight = "secondary"
    else:
        default_weight = "unknown"

    return {
        "source_type": source_type,
        "url": url,
        "review_weight": default_weight,
        "review_note": "Check provenance before using this source for a central claim.",
    }


def build_source_ledger(topic: str, sources: list[dict[str, Any]]) -> dict[str, str]:
    """Build a markdown source ledger from normalized source records."""

    if not topic.strip():
        raise ValueError("topic is required")

    rows = [
        "| Source ID | Title | Type | Retrieved | Notes |",
        "|---|---|---|---|---|",
    ]
    for source in sources:
        rows.append(
            "| {source_id} | [{title}]({url}) | {source_type} | {retrieved_at} | {notes} |".format(
                source_id=source.get("source_id", "SRC-UNKNOWN"),
                title=str(source.get("title", "")).replace("|", "\\|"),
                url=source.get("url", ""),
                source_type=str(source.get("source_type", "")).replace("|", "\\|"),
                retrieved_at=source.get("retrieved_at", ""),
                notes=str(source.get("notes", "")).replace("|", "\\|"),
            )
        )

    return {
        "topic": topic.strip(),
        "path": f"llm-wiki/raw/{slugify_topic(topic)}_source_ledger.md",
        "markdown": "\n".join(rows),
    }


def prepare_aiq_research_request(
    question: str,
    objective: str = "deep research report",
    source_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Prepare the request contract for the official NVIDIA AI-Q research skill."""

    if not question.strip():
        raise ValueError("question is required")

    return {
        "question": question.strip(),
        "objective": objective.strip() or "deep research report",
        "source_ids": source_ids or [],
        "aiq_server_url": os.getenv("AIQ_SERVER_URL", "http://localhost:8000"),
        "expected_skill": "aiq-research",
        "expected_flow": [
            "health",
            "chat or submit",
            "poll if a job ID is returned",
            "write cited report into the source ledger or draft brief",
        ],
        "required_disclosure": "Record whether AI-Q was live, unavailable, or skipped.",
    }
