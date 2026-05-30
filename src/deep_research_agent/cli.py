"""Command-line entry point for the workshop agent."""

from __future__ import annotations

import argparse
import json

from deep_research_agent.agent import invoke_task

DEFAULT_TASK = (
    "Compare three current approaches to long-running AI research agents. "
    "Produce a source-backed brief, source ledger, open questions, and run log."
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the long-running research-agent harness.")
    parser.add_argument("task", nargs="*", help="Research task for the agent.")
    args = parser.parse_args()

    task = " ".join(args.task).strip() or DEFAULT_TASK
    try:
        result = invoke_task(task)
    except RuntimeError as error:
        parser.exit(2, f"Setup error: {error}\n")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
