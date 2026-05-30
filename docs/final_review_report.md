# Final Code And Copywriting Review

Date: May 30, 2026

Scope reviewed:

- Workshop package and console command
- Jupyter walkthrough
- Static workshop page
- Local skills
- LLM Wiki templates
- Tests, docs, and source links

## Executive Assessment

The repo is now ready as a workshop starter from a repository checkout. The
implementation and the teaching copy agree on the core artifact contract:
source ledger, open questions, run log, and draft research brief. The notebook
executes without model credentials, the source-ledger path convention is
topic-specific, the AI-Q lane is clearly labeled as a local teaching shim unless
the official NVIDIA skills are installed, and the copy no longer talks down to
the audience.

The repo should be taught and distributed as a checkout, not as a standalone
wheel. The Python package and CLI are UV-installable, but the hands-on workshop
also depends on `.agents/skills/`, `llm-wiki/`, `docs/`, `site/`, and
`notebooks/`. The lockfile is intentionally omitted and ignored; participants
should run `uv sync --all-groups` from the checkout.

## Verification Results

Commands run from `/Users/marc/Documents/New project/deep-wiki-drug-agent`:

```bash
uv run ruff check .
uv run pytest -q
uv run --group notebook jupyter nbconvert --execute --to notebook --output /private/tmp/deep_research_agent_fixed.executed.ipynb notebooks/deep_research_agent_walkthrough.ipynb
uv build
```

Results:

- Ruff: passed.
- Pytest: `13 passed`.
- Notebook execution: passed.
- Package build: passed.

## Fixes Implemented

### Artifact contract aligned

The deterministic notebook now writes all four workshop artifacts:

- `llm-wiki/raw/long_running_ai_research_agents_source_ledger.md`
- `llm-wiki/raw/long_running_ai_research_agents_open_questions.md`
- `llm-wiki/raw/long_running_ai_research_agents_run_log.md`
- `llm-wiki/wiki/research-briefs/long_running_ai_research_agents.md`

The structure test now checks that the notebook names the open-questions and
run-log paths, so this cannot silently regress.

### Source-ledger paths made topic-specific

`build_source_ledger()` now returns a topic-specific path using
`slugify_topic()`. The test suite now expects
`llm-wiki/raw/deep_agents_source_ledger.md` for the `deep agents` topic.

### Checkout delivery model documented

The README now says explicitly that the repository checkout is the workshop
delivery artifact. This resolves the package-build ambiguity: `uv build` is
valid for the Python package, but the wheel is not the complete workshop.

The README also documents the `uv.lock` decision. The repo keeps
`pyproject.toml` as the dependency contract and lets UV create a local lockfile
for each checkout.

### AI-Q lane clarified

The local `.agents/skills/aiq-research/SKILL.md` now states that it is a
teaching shim, not a vendored copy of NVIDIA's official AI-Q skill
implementation. The tutorial explains that live AI-Q research requires
NVIDIA's official `aiq-deploy` and `aiq-research` skills plus a reachable AI-Q
backend.

Sources checked:

- NVIDIA AI-Q Agent Skills docs: https://docs.nvidia.com/aiq-blueprint/latest/integration/agent-skills.html
- NVIDIA technical blog on specialized AI-Q deep research skills: https://developer.nvidia.com/blog/add-a-specialized-deep-research-skill-to-agent-harnesses/

### Copy tightened

The remaining "basic software engineers" phrasing was replaced with
"software engineers new to agent frameworks." The old "dossier" wording was
replaced with the actual workshop artifacts: brief, source ledger, open
questions, and run log.

## Current Readiness

Status: ready for participant checkout after publishing the current local state
to GitHub.

Recommended facilitator flow:

1. Send the GitHub repo as the setup link.
2. Have participants run `uv sync --all-groups`.
3. Start with the static page for orientation.
4. Use the notebook as the hands-on path.
5. Treat the live Deep Agents and AI-Q cells as optional extension lanes.
