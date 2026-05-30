---
name: aiq-research
description: Use this skill when a research task needs deeper multi-source synthesis, citation-rich reporting, or enterprise/internal data search through NVIDIA AI-Q.
---

# AI-Q Research

This workshop file is a local teaching shim for the AI-Q research lane. It
shows the request contract the harness should prepare. It is not a vendored
copy of NVIDIA's official AI-Q skill implementation.

Use this skill when the coordinator asks for AI-Q research through a reachable
NVIDIA AI-Q Blueprint backend. For a live backend, install NVIDIA's official
`aiq-deploy` and `aiq-research` skills from the NVIDIA Agent Skills catalog and
point `AIQ_SERVER_URL` at the running AI-Q service.

## Preconditions

- A running AI-Q server is reachable at `AIQ_SERVER_URL`.
- The task is a research synthesis task, not a direct source lookup.
- For a local backend, the default URL is `http://localhost:8000`.

## Use Cases

- Multi-document synthesis.
- Internal source search where raw documents should remain inside a governed environment.
- Source-attributed decision briefs.
- Long-running research jobs that may return a job ID and require polling.

## Workshop Mode

If AI-Q is unavailable:

1. State that AI-Q is unavailable.
2. Continue with local source-ledger work.
3. Add an `AI-Q follow-up` section to the final brief.

## Output Contract

Return:

- research question
- sources searched
- cited findings
- confidence and caveats
- unresolved questions
- whether AI-Q was live, unavailable, or skipped

## Official Skill Split

NVIDIA publishes two official AI-Q skills:

- `aiq-deploy` starts, validates, troubleshoots, and stops AI-Q infrastructure.
- `aiq-research` sends research requests to a reachable AI-Q backend and polls jobs.

Use `aiq-deploy` for setup. Use `aiq-research` for research.
