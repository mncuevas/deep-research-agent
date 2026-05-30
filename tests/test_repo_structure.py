from __future__ import annotations

import json
from pathlib import Path

from deep_research_agent.agent import create_agent
from deep_research_agent.config import load_config


def test_required_workshop_files_exist():
    config = load_config()
    required = [
        config.repo_root / "docs" / "tutorial.md",
        config.repo_root / "docs" / "architecture_memo.md",
        config.repo_root / "docs" / "source_links.md",
        config.repo_root / ".agents" / "skills" / "research-scout" / "SKILL.md",
        config.repo_root / ".agents" / "skills" / "source-ledger" / "SKILL.md",
        config.repo_root / ".agents" / "skills" / "wiki-curator" / "SKILL.md",
        config.repo_root / ".agents" / "skills" / "aiq-research" / "SKILL.md",
        config.repo_root / "llm-wiki" / "agent" / "TASK_PACKET_TEMPLATE.md",
        config.repo_root / "llm-wiki" / "wiki" / "research-briefs" / "TEMPLATE.md",
        config.repo_root / "notebooks" / "deep_research_agent_walkthrough.ipynb",
        config.repo_root / "site" / "index.html",
        config.repo_root / "site" / "styles.css",
        config.repo_root / "evals" / "eval_cases.csv",
    ]

    missing = [path for path in required if not path.exists()]
    assert missing == []


def test_skill_frontmatter_names_are_present():
    config = load_config()
    skill_files = sorted((config.repo_root / ".agents" / "skills").glob("*/SKILL.md"))

    assert skill_files
    for skill_file in skill_files:
        text = skill_file.read_text()
        assert text.startswith("---")
        assert "name:" in text
        assert "description:" in text


def test_docs_reference_agent_harness():
    config = load_config()
    tutorial = Path(config.repo_root / "docs" / "tutorial.md").read_text()

    assert "agent harness" in tutorial.lower()
    assert "Deep Agents" in tutorial
    assert "LLM Wiki" in tutorial


def test_notebook_walkthrough_is_valid_json_and_teaches_harness():
    config = load_config()
    notebook_path = config.repo_root / "notebooks" / "deep_research_agent_walkthrough.ipynb"
    notebook = json.loads(notebook_path.read_text())

    assert notebook["nbformat"] == 4
    markdown = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "markdown"
    )
    assert "agent harness" in markdown.lower()
    assert "Deep Agents" in markdown
    assert "LangChain Deep Agents framework" in markdown
    assert "LLM Wiki" in markdown
    assert "create_deep_agent" in markdown
    assert "Optional live Deep Agents run" in markdown

    code = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    )
    assert "prepare_aiq_research_request" in code
    assert "uv" in markdown.lower()


def test_static_site_teaches_project_flow():
    config = load_config()
    html = (config.repo_root / "site" / "index.html").read_text()

    assert "Deep Agents Walkthrough" in html
    assert "create_deep_agent" in html
    assert "AI-Q" in html


def test_create_agent_reports_missing_openai_credentials(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_ADMIN_KEY", raising=False)
    monkeypatch.setenv("DEEP_AGENTS_MODEL", "openai:gpt-5.4")

    try:
        create_agent()
    except RuntimeError as error:
        assert "OPENAI_API_KEY" in str(error)
    else:
        raise AssertionError("Expected missing OpenAI credentials to raise RuntimeError")
