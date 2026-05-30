"""Long-running research-agent harness construction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from deep_research_agent.config import AgentConfig, load_config, missing_model_credentials
from deep_research_agent.tools import (
    build_source_ledger,
    classify_source,
    create_task_packet,
    prepare_aiq_research_request,
    record_source,
)

COORDINATOR_PROMPT = """You are a long-running research harness coordinator.

Your job is to turn a broad research task into reviewable workspace artifacts.

Operating rules:
- Use write_todos before complex work.
- Delegate specialized source work to subagents.
- Treat source outputs and AI-Q reports as evidence inputs.
- Preserve source IDs, URLs, dates, gaps, and uncertainty labels.
- Write only staged wiki artifacts under /workspace/llm-wiki/.
- Final response must list changed files, source IDs used, open questions, and reviewer warnings.
"""


def _skills_source(config: AgentConfig) -> str:
    return str(config.skills_dir)


def _workspace_backend(config: AgentConfig) -> Any:
    """Build the Deep Agents filesystem backend.

    Imports are lazy so the rest of the package and unit tests remain usable
    before optional agent runtime dependencies are installed.
    """

    from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend

    return CompositeBackend(
        default=StateBackend(),
        routes={
            "/workspace/": FilesystemBackend(root_dir=str(config.repo_root), virtual_mode=True),
        },
    )


def _workspace_permissions() -> list[Any]:
    """Allow only scoped reads/writes in the virtual workspace."""

    from deepagents import FilesystemPermission

    return [
        FilesystemPermission(
            operations=["read", "write"],
            paths=["/workspace/.env"],
            mode="deny",
        ),
        FilesystemPermission(
            operations=["read"],
            paths=["/workspace/**"],
            mode="allow",
        ),
        FilesystemPermission(
            operations=["write"],
            paths=[
                "/workspace/llm-wiki/wiki/**",
                "/workspace/llm-wiki/raw/**",
            ],
            mode="allow",
        ),
        FilesystemPermission(
            operations=["write"],
            paths=["/**"],
            mode="deny",
        ),
    ]


def _reviewer_permissions() -> list[Any]:
    """Read-only permissions for the skeptic reviewer subagent."""

    from deepagents import FilesystemPermission

    return [
        FilesystemPermission(
            operations=["write"],
            paths=["/**"],
            mode="deny",
        ),
        FilesystemPermission(
            operations=["read"],
            paths=["/workspace/**"],
            mode="allow",
        ),
        FilesystemPermission(
            operations=["read"],
            paths=["/**"],
            mode="deny",
        ),
    ]


def build_subagents(config: AgentConfig) -> list[dict[str, Any]]:
    """Return the specialized subagent specs used by the tutorial harness."""

    skills = [_skills_source(config)]
    return [
        {
            "name": "source-scout",
            "description": "Collects source records and prepares a source ledger.",
            "system_prompt": (
                "Collect source records for the topic. Prefer official docs, source repositories, "
                "release notes, standards, and primary project materials. Return normalized "
                "source records with stable source IDs and retrieval dates."
            ),
            "tools": [record_source, classify_source, build_source_ledger],
            "skills": skills,
        },
        {
            "name": "synthesis-writer",
            "description": "Writes a concise draft brief from source-backed notes.",
            "system_prompt": (
                "Turn the task packet and source ledger into a short draft brief. Keep claims "
                "source-backed. Put unresolved questions in their own section."
            ),
            "tools": [create_task_packet, build_source_ledger],
            "skills": skills,
        },
        {
            "name": "skill-router",
            "description": "Prepares requests for external skills such as NVIDIA AI-Q.",
            "system_prompt": (
                "Use this subagent when a task needs a skill-backed backend. Prepare a clear "
                "request contract, name the backend, record whether it was live or unavailable, "
                "and keep returned reports as source inputs."
            ),
            "tools": [prepare_aiq_research_request],
            "skills": skills,
        },
        {
            "name": "skeptic-reviewer",
            "description": "Read-only reviewer that checks staged claims and sources.",
            "system_prompt": (
                "Review staged wiki artifacts. Do not edit. Flag unsupported claims, missing "
                "source IDs, overconfident wording, hidden failures, and unresolved questions."
            ),
            "permissions": _reviewer_permissions(),
            "skills": skills,
        },
    ]


def create_agent(config: AgentConfig | None = None) -> Any:
    """Create the Deep Agents harness."""

    from deepagents import create_deep_agent

    config = config or load_config()
    if missing := missing_model_credentials(config):
        raise RuntimeError(f"{missing} Set it in .env or choose another DEEP_AGENTS_MODEL.")

    return create_deep_agent(
        model=config.model,
        tools=[
            create_task_packet,
            record_source,
            classify_source,
            build_source_ledger,
            prepare_aiq_research_request,
        ],
        backend=_workspace_backend(config),
        permissions=_workspace_permissions(),
        skills=[_skills_source(config)],
        subagents=build_subagents(config),
        system_prompt=COORDINATOR_PROMPT,
    )


def invoke_task(task: str, config: AgentConfig | None = None) -> Any:
    """Invoke the agent on a research task."""

    agent = create_agent(config)
    return agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Use /workspace/llm-wiki/agent/TASK_PACKET_TEMPLATE.md as the output "
                        f"contract. {task}"
                    ),
                }
            ]
        }
    )


def repo_relative(path: Path) -> str:
    """Return a stable repository-relative path for user-facing messages."""

    config = load_config()
    return str(path.relative_to(config.repo_root))
