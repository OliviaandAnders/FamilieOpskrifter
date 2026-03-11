"""
FamilieOpskrifter Multi-Agent System
=====================================
A 4-agent pipeline for automating changes to the recipe website.

Agents:
  Conductor  — orchestrates the full pipeline via the Agent tool
  Planner    — analyzes request, creates implementation plan (no code)
  Coder      — implements the plan in code
  Reviewer   — reviews code against plan, approves or requests revision

Usage:
  python scripts/agents/main.py "Add a TIME field validation warning to the build script"

Requirements:
  pip install claude-agent-sdk
  Set ANTHROPIC_API_KEY in your environment.
"""
from __future__ import annotations

import sys
import os
import anyio

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from conductor import run


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        print("ERROR: No task provided.")
        print('Usage: python scripts/agents/main.py "your task here"')
        return 1

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        return 1

    request = " ".join(sys.argv[1:])
    anyio.run(run, request)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
