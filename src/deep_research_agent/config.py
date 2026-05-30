"""Project configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
WIKI_ROOT = REPO_ROOT / "llm-wiki"


@dataclass(frozen=True)
class AgentConfig:
    """Runtime configuration for the research-agent harness."""

    model: str
    repo_root: Path
    skills_dir: Path
    wiki_root: Path
    aiq_server_url: str


def load_config() -> AgentConfig:
    """Load configuration from environment variables with workshop-safe defaults."""

    load_dotenv(REPO_ROOT / ".env", override=False)
    return AgentConfig(
        model=os.getenv("DEEP_AGENTS_MODEL", "openai:gpt-5.4"),
        repo_root=REPO_ROOT,
        skills_dir=SKILLS_DIR,
        wiki_root=WIKI_ROOT,
        aiq_server_url=os.getenv("AIQ_SERVER_URL", "http://localhost:8000"),
    )


def missing_model_credentials(config: AgentConfig) -> str | None:
    """Return a setup hint when the configured model provider is missing credentials."""

    provider = config.model.split(":", maxsplit=1)[0].lower()
    if provider == "openai" and not (
        os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_ADMIN_KEY")
    ):
        return "OPENAI_API_KEY or OPENAI_ADMIN_KEY is required for OpenAI models."
    return None
