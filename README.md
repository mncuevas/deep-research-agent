# Deep Research Agent Starter

An open-source workshop repo for building a long-running research agent with
Deep Agents, filesystem-backed memory, source ledgers, subagents, and skills.

The project combines:

- **Deep Agents** as the harness: planning, files, skills, permissions, and subagents.
- **LLM Wiki** as the workspace: draft status, source IDs, run logs, and reusable briefs.
- **Deterministic source helpers** for task packets, source records, source ledgers, and AI-Q request contracts.
- **Skills** for research scouting, source-ledger discipline, wiki curation, and optional NVIDIA AI-Q research.

The default path is local and deterministic. Live model calls and AI-Q are extension paths.

## Quick Start

```bash
uv sync --all-groups
cp .env.example .env
uv run pytest -q
```

Run a scaffolded agent task after adding model credentials:

```bash
uv run deep-research-agent "Compare three current approaches to long-running AI research agents. Produce a source-backed brief, source ledger, open questions, and run log."
```

## Walkthrough Options

There are two workshop surfaces:

- [Static workshop page](site/index.html) for the shareable handout.
- [Jupyter notebook](notebooks/deep_research_agent_walkthrough.ipynb) for an executable, cell-by-cell walkthrough.

Run the notebook:

```bash
uv sync --group notebook
uv run --group notebook jupyter lab notebooks/deep_research_agent_walkthrough.ipynb
```

The notebook is safe to run without model credentials. It uses deterministic local
helpers by default and only attempts a live Deep Agents invocation if model
credentials are configured.

Execute the notebook non-interactively:

```bash
uv run --group notebook jupyter nbconvert \
  --execute \
  --to notebook \
  --output /tmp/deep_research_agent_walkthrough.executed.ipynb \
  notebooks/deep_research_agent_walkthrough.ipynb
```

## Repo Layout

```text
.
├── .agents/skills/              # Agent skills
├── docs/                        # Tutorial, architecture memo, source links
├── evals/                       # Lightweight workshop eval cases
├── llm-wiki/                    # Research workspace starter
├── notebooks/                   # Executable Jupyter walkthrough
├── site/                        # Static workshop page
├── src/deep_research_agent/     # Python package
└── tests/                       # Unit and structure tests
```

## Workshop Flow

1. Explain the LangChain Deep Agents framework.
2. Inspect the UV package and console entry point.
3. Read the `create_deep_agent` constructor.
4. Inspect the coordinator prompt.
5. Run deterministic source tools.
6. Read skills and subagent specs.
7. Prepare an optional AI-Q request contract.
8. Stage example LLM Wiki artifacts.
9. Optionally run the live Deep Agents harness.
10. Review files, source IDs, open questions, and run notes.

## Verification

Run these before teaching or publishing changes:

```bash
uv sync --all-groups
uv run ruff check .
uv run pytest -q
uv run --group notebook jupyter nbconvert \
  --execute \
  --to notebook \
  --output /tmp/deep_research_agent_walkthrough.executed.ipynb \
  notebooks/deep_research_agent_walkthrough.ipynb
uv build
```

## Boundary

This repo teaches software architecture for research agents. Generated briefs are
draft artifacts until reviewed by an accountable human.
