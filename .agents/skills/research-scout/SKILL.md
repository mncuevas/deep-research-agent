---
name: research-scout
description: Use this skill when collecting sources for a research brief, source ledger, or long-running agent run.
---

# Research Scout

Use this skill to collect source-backed material without turning the search step into
the final answer.

## Source Order

Prefer:

1. Official documentation
2. Source repositories
3. Release notes
4. Standards or specifications
5. Primary announcements
6. Secondary analysis

## Rules

- Record a source ID for every source used in a central claim.
- Keep source notes separate from the draft report.
- Prefer dates, versions, commit IDs, and URLs over vague references.
- Mark sources as primary, secondary, or unknown.
- Preserve disagreement between sources.
- Record failed searches or unavailable sources in the run log.

## Output Shape

```markdown
### Source Record
- Source ID:
- Title:
- URL:
- Type:
- Retrieved:
- Notes:

### Coverage Gaps
- ...
```
