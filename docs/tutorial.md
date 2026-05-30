# Tutorial: Build A Long-Running Research Agent

Audience: software engineers who know Python and APIs, but do not need prior
agent-framework experience.

Time: 75-90 minutes.

Outcome: participants build a runnable Deep Agents research harness that can
take a broad task, create a task packet, keep a source ledger, use skills,
delegate focused work to subagents, optionally prepare an AI-Q request, and
stage reviewable LLM Wiki artifacts.

## Introduction

Some questions are not single tool calls. They are investigations. A useful
research agent has to assemble evidence, normalize sources, keep intermediate
work out of the main prompt, draft an artifact, and leave enough state behind
for a human to review what happened.

This tutorial shows that pattern with LangChain Deep Agents. Deep Agents gives
you the harness: planning, filesystem state, subagents, skills, permissions,
and a repeatable invocation path. The LLM Wiki gives you the workspace: source
IDs, draft files, open questions, run logs, and review notes.

The default path is local and deterministic. Participants can complete the
notebook without live model credentials. A live Deep Agents run and AI-Q are
extension lanes at the end.

## What You'll Build

You will build a small research system with these pieces:

- a UV-installable Python package
- a `deep-research-agent` console command
- deterministic source tools for task packets, source records, ledgers, and
  AI-Q request contracts
- four local skills: `research-scout`, `source-ledger`, `wiki-curator`, and
  `aiq-research`
- four subagents: source scout, synthesis writer, skill router, and read-only
  reviewer
- an LLM Wiki workspace for staged artifacts
- an executable notebook walkthrough
- tests that verify the package, docs, notebook, site, skills, and helpers

The first run compares current approaches to long-running AI research agents.
Teams can swap the topic after the baseline works, but the artifact contract
should stay the same.

## Set Up

Install the repo with UV and run the basic verification path:

```bash
uv sync --all-groups
cp .env.example .env
uv run ruff check .
uv run pytest -q
```

The `.env` file is only needed for the optional live run. The deterministic
notebook cells do not call a model or AI-Q.

Open the notebook:

```bash
uv run --group notebook jupyter lab notebooks/deep_research_agent_walkthrough.ipynb
```

Or execute it non-interactively:

```bash
uv run --group notebook jupyter nbconvert \
  --execute \
  --to notebook \
  --output /tmp/deep_research_agent_walkthrough.executed.ipynb \
  notebooks/deep_research_agent_walkthrough.ipynb
```

## Install And Run The Baseline

Start with the package surface. The repo should install as a normal Python
project, expose a console command, and keep the workshop code under `src/`.

```bash
uv run deep-research-agent --help
```

The live command needs model credentials. Without credentials, the package
should fail clearly instead of pretending it ran:

```bash
uv run deep-research-agent \
  "Compare three current approaches to long-running AI research agents."
```

For the workshop, begin with the notebook because it walks through the same
system without making the group wait on a model call.

## Understand The Harness

The core construction happens in `src/deep_research_agent/agent.py`.

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
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
```

Read this as the agent's contract. The model is the reasoning engine. Tools are
the callable operations. The backend is where state and files live.
Permissions define what can be read or written. Skills are reusable procedures.
Subagents isolate focused work. The system prompt defines the coordinator's
job.

This is the first key distinction in the workshop: a prompt asks for an answer;
an agent harness defines the work environment that produces an answer and the
artifacts needed to inspect it.

## Add The Research Task

Use this first task:

```text
Compare three current approaches to long-running AI research agents.

Use public sources only. Prefer official docs, repositories, release notes,
and specifications. Produce:

1. A short research brief.
2. A source ledger.
3. Open questions.
4. A run log.

Every important claim needs a source ID. Record unavailable skills or failed
tool calls directly in the run log.
```

The task packet turns that request into a structured contract. It names the
topic, scope, deliverable, required files, and review rules. The packet is
small, but it prevents the run from becoming just another free-form response.

## Add Deterministic Source Tools

The first source helpers are deliberately ordinary Python functions:

- `create_task_packet`
- `record_source`
- `classify_source`
- `build_source_ledger`
- `prepare_aiq_research_request`

`record_source` turns a title and URL into a normalized source record with a
stable source ID. `build_source_ledger` turns those records into markdown. This
lets participants see evidence handling before any live model call.

The teaching point is practical: keep low-level operations typed and reviewable,
then let the agent compose them.

## Add Skills

Skills turn repeatable procedures into loadable harness components.

| Skill | Job |
|---|---|
| `research-scout` | Collect source records without collapsing search into the final answer. |
| `source-ledger` | Keep claims tied to source IDs, caveats, and review notes. |
| `wiki-curator` | Stage durable LLM Wiki pages and raw notes. |
| `aiq-research` | Prepare the optional AI-Q research path. |

A skill is not a Python function. It is procedural guidance the agent can read
when a task needs that behavior. Skills are good for policies, output
contracts, review rules, and backend-specific instructions that should be
visible to the team.

## Add Subagents

Use subagents when a narrower context helps.

| Subagent | Job | Tools | Writes? |
|---|---|---|---|
| `source-scout` | Create source records and ledger entries. | source helpers | No |
| `synthesis-writer` | Draft the brief from the packet and ledger. | source helpers | Staged paths only |
| `skill-router` | Prepare AI-Q request contracts. | AI-Q request helper | No |
| `skeptic-reviewer` | Read-only review of staged files. | filesystem read | No |

The main coordinator should not hold every detail from every source. Subagents
let the coordinator ask for focused work and receive concise results. The
reviewer subagent is intentionally read-only so review cannot silently rewrite
the artifact it is checking.

## Add A Source Lane

The baseline source lane uses public URLs and deterministic source records. In
a real environment, this is where you would add a search API, an internal wiki,
an MCP server, a document store, or a backend such as AI-Q.

The pattern is the same:

1. Define the source boundary.
2. Normalize every returned item into a stable record.
3. Preserve source IDs through the brief.
4. Record failed calls and unavailable systems.
5. Keep draft claims draft until reviewed.

Do not start by building a large search abstraction. Start with one source, one
record shape, and one ledger. Once the ledger is useful, add more sources.

## Add AI-Q As A Skill Lane

AI-Q is optional in this workshop. Treat it as a specialized backend skill, not
as a shortcut around review.

The local helper `prepare_aiq_research_request` creates a request contract:

- research question
- objective
- source IDs already gathered
- expected AI-Q server URL
- expected `aiq-research` skill
- required disclosure: live, unavailable, or skipped

NVIDIA publishes two official AI-Q skills:

- `aiq-deploy` for setup, validation, troubleshooting, and shutdown
- `aiq-research` for research requests, job polling, and cited reports

If AI-Q is unavailable, the agent should state that directly and continue with
local source-ledger work. A missing backend is a run note, not a failed
workshop.

## Produce Reviewable Files

The minimum output should create or sketch:

```text
llm-wiki/wiki/research-briefs/<topic>.md
llm-wiki/raw/<topic>_source_ledger.md
llm-wiki/raw/<topic>_open_questions.md
llm-wiki/raw/<topic>_run_log.md
```

The brief should include:

- summary
- scope
- source-ledger summary
- findings
- contradictions or disagreements
- open questions
- run notes
- reviewer checklist

The notebook writes deterministic example artifacts first. A live run can
replace them later.

## Inspect The Run

Before trusting any final answer, inspect the files. Ask:

- Which sources support the central claims?
- Which claims are still draft?
- Which tool calls or backend skills were unavailable?
- Which files changed?
- Which open questions remain?
- Did the reviewer flag unsupported claims?

For production systems, this same idea expands into traces, evals, policy
checks, and governed asset registration. For the workshop, the file tree is the
trace beginners can understand.

## Optional Live Run

After adding model credentials to `.env`, run:

```bash
uv run deep-research-agent \
  "Compare three current approaches to long-running AI research agents. \
  Use public sources only. Use AI-Q only if available; otherwise mark it \
  unavailable. Stage a source-backed brief, source ledger, open questions, \
  and run log."
```

Expected behavior:

1. The coordinator creates a plan.
2. The coordinator delegates source, synthesis, skill-routing, and review work.
3. Subagents return concise intermediate artifacts.
4. The wiki curator stages the brief and raw notes.
5. The reviewer checks claims and source IDs.
6. The coordinator reports changed files and unresolved questions.

## Debrief

Ask participants:

- Which part was agent work, and which part was harness design?
- Which files made the run easier to inspect?
- Which claim should stay draft?
- What did subagents keep out of the main context?
- Where would AI-Q add value over local source helpers?
- Which skill would your team write next?

## Going Further

For a longer workshop:

- Install official `aiq-deploy` and `aiq-research` from the NVIDIA skills catalog.
- Add a NeMo Retriever or RAG Blueprint backend as another skill lane.
- Add an eval that checks every central claim has a source ID.
- Add an async subagent path and poll for completion.
- Add a LangGraph approval interrupt before promoting a draft brief.
- Add a skill card review before installing any new skill.
- Add a real source connector for a team-owned corpus or MCP server.

## Sources

- LangChain Deep Agents overview: https://docs.langchain.com/oss/python/deepagents/overview
- LangChain Deep Agents subagents: https://docs.langchain.com/oss/python/deepagents/subagents
- Deep Agents API reference: https://reference.langchain.com/python/deepagents/graph/create_deep_agent
- NVIDIA Agent Skills catalog: https://github.com/NVIDIA/skills
- NVIDIA AI-Q Agent Skills docs: https://docs.nvidia.com/aiq-blueprint/latest/integration/agent-skills.html
- Agent Skills specification: https://github.com/agentskills/agentskills
