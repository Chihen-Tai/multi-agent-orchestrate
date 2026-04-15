"""
Multi-agent orchestrator entry point.

Usage:
  python main.py "your task description" --type general
  python main.py "design a caching layer" --type architecture
  python main.py "refactor auth module" --type high_stakes
  python main.py "document the API" --type documentation

Task types: general, architecture, high_stakes, documentation
"""

import argparse
import sys
from router import route, VALID_TYPES
from synthesizer import synthesize


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Multi-agent orchestrator: routes tasks to Codex, Copilot, and Gemini CLIs."
    )
    parser.add_argument("task", help="The task description to delegate.")
    parser.add_argument(
        "--type",
        dest="task_type",
        choices=VALID_TYPES,
        default="general",
        help=f"Task type controlling which agents are used. Choices: {VALID_TYPES}. Default: general",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Per-agent timeout in seconds (default: 120).",
    )
    args = parser.parse_args()

    print(f"\nOrchestrating [{args.task_type}] task...")
    print(f"Task: {args.task}\n")

    try:
        results = route(args.task, args.task_type)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    report = synthesize(args.task, args.task_type, results)
    print(report)


if __name__ == "__main__":
    main()
