# Notebooks

Start the walkthrough with:

```bash
uv sync --group notebook
uv run --group notebook jupyter lab notebooks/deep_research_agent_walkthrough.ipynb
```

The notebook is designed for workshop use:

- no live model call unless credentials are configured
- deterministic local source helpers in the default cells
- optional final cell for a real agent invocation
