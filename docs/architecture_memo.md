# Architecture Memo: Long-Running Research Agent

## Audience

Software engineers who want a practical pattern for research agents: how to
structure the run, how to keep sources visible, and how to add skills without
making the workflow opaque.

## Teaching Goal

Teach participants to build an autonomous research harness that produces
reviewable files.

The key insight:

> A useful research agent leaves behind a workspace another person can inspect.

## Core Components

1. Deep Agents
   - Harness: planning, filesystem, skills, subagents, permissions.

2. LLM Wiki
   - Workspace: source IDs, draft status, run logs, open questions.

3. Source helpers
   - Deterministic functions for task packets, source records, ledgers, and AI-Q requests.

4. Skills
   - Reusable instructions for research scouting, ledger writing, wiki curation, and AI-Q.

5. Subagents
   - Separate source collection, synthesis, skill routing, and read-only review.

## Workshop Flow

1. Define the agent harness.
2. Inspect the task packet and workspace.
3. Create source records and a source ledger.
4. Add or inspect skills.
5. Add subagents.
6. Optionally prepare an AI-Q research request.
7. Stage a draft research brief.
8. Review files, source IDs, open questions, and run notes.

## Why AI-Q Is A Skill

AI-Q is a specialized research backend. The workshop should teach the pattern
that lets a harness use it:

- local work succeeds without a live AI-Q server
- `aiq-deploy` owns backend setup and validation
- `aiq-research` owns research calls and job polling
- returned reports become source inputs, not automatic final truth

## Success Criteria

By the end, participants can explain:

- what an agent harness is
- how skills differ from tools
- when subagents help
- why a source ledger matters
- how to turn agent output into reviewable files
- where AI-Q adds value over local source helpers
