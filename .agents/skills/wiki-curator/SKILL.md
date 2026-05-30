---
name: wiki-curator
description: Use this skill when creating or updating LLM Wiki pages, research briefs, source ledgers, or staged research notes.
---

# Wiki Curator

Use this skill to stage durable LLM Wiki updates.

## Read First

Before writing, read:

1. `/workspace/llm-wiki/README.md`
2. `/workspace/llm-wiki/INDEX.md`
3. `/workspace/llm-wiki/TRUST_MODEL.md`
4. `/workspace/llm-wiki/agent/TASK_PACKET_TEMPLATE.md`

## Write Rules

- Write only under `/workspace/llm-wiki/wiki/` and `/workspace/llm-wiki/raw/`.
- New briefs start as `status: draft`.
- Every important claim needs a source ID or must be marked `needs_review`.
- Keep raw tool output in `/workspace/llm-wiki/raw/`.
- Keep durable synthesis in `/workspace/llm-wiki/wiki/`.
- Preserve uncertainty and contradictions.

## Brief Sections

Each research brief should include:

1. Summary
2. Scope
3. Source ledger summary
4. Findings
5. Contradictions or disagreements
6. Open questions
7. Run notes
8. Reviewer checklist
