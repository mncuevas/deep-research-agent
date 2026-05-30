# Delivery Options

## Recommendation

Use both, but for different jobs:

- **Static page**: send before the workshop and use as the landing surface during setup.
- **Notebook**: use for the live hands-on path once everyone has the repo open.

The static page gives participants a quick mental model and keeps the project from feeling like a folder of scripts. The notebook is better once they need to inspect code, run mocked tools, and optionally invoke the live agent.

## Static Page Strengths

- Easy to share.
- Works without Python, credentials, or setup.
- Good for orienting basic software engineers.
- Better for showing the overall flow: harness, wiki, skills, subagents, dossier.

## Notebook Strengths

- Executable.
- Better for live teaching.
- Lets participants inspect tool wrappers and outputs.
- Can use mocked data first, then switch to a live model run.

## What Not To Do

Do not make the first participant experience a live autonomous model run. Start with the harness anatomy, deterministic tool outputs, and the dossier contract. The live agent should be the final optional cell.
