from __future__ import annotations

import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, ResultMessage


PROJECT_CONTEXT = """\
FamilieOpskrifter is a static family recipe website.

Tech stack:
- Frontend: Vanilla JavaScript, HTML5, CSS3 (no frameworks)
- Build tool: Python 3 (scripts/build_recipes.py)
- Data: data/recipes.json and data/recipes.js (generated)
- Content: recipe.txt files under content/<category>/<recipe-slug>/

Recipe file format:
  TITLE: Example Dish
  DESCRIPTION: Brief description
  SERVINGS: 4
  TIME: 45 min
  INGREDIENTS:
  - 500 g ingredient
  METHOD:
  1. Step one.
  NOTER:
  - Optional note.

Key files:
- scripts/build_recipes.py  — scans content/, generates data/recipes.json
- index.html                — recipe browser with search and filtering
- recipe.html               — recipe detail page (?id=category/slug)
- wheel.html                — recipe roulette spin wheel
- styles.css                — all styling
"""

PLANNER_PROMPT = """\
You are a senior software architect and planner for the FamilieOpskrifter recipe website.

Your ONLY job is to analyze requests and produce clear implementation plans.
You must NEVER write actual code — plans only.

For every request, output:

## Plan
<high-level description of the approach>

## Files to touch
- <file path>: <what changes and why>

## Steps
1. <step>
2. <step>

## Potential issues
- <issue>
"""

CODER_PROMPT = """\
You are an expert Python and JavaScript developer working on the FamilieOpskrifter recipe website.

You will receive a task and a plan. Implement the plan exactly.

For each file you change or create, use this format:

### FILE: <path/to/file>
```
<complete file contents>
```

Write clean, production-quality code that matches the existing style in the project.
Use the Read tool to inspect existing files before modifying them.
"""

REVIEWER_PROMPT = """\
You are a senior code reviewer for the FamilieOpskrifter recipe website.

You will receive a task, a plan, and the implemented code. Review thoroughly.

Output:

## Verdict
APPROVED or REVISION NEEDED

## Comments
<observations>

## Issues (only if REVISION NEEDED)
- <specific issue>

Be constructive. Approve if the code is correct and matches the plan.
"""


async def run(request: str) -> None:
    print("=" * 60)
    print("[Conductor] Starting pipeline")
    print(f"[Conductor] Request: {request}")
    print("=" * 60)

    conductor_prompt = f"""\
You are the Conductor of a multi-agent software pipeline for the FamilieOpskrifter recipe website.

Project context:
{PROJECT_CONTEXT}

User request:
{request}

Your job is to coordinate the pipeline in this exact order:

1. Use the `planner` agent to create an implementation plan for the request.
   Pass it the full project context and the user request.

2. Use the `coder` agent to implement the plan.
   Pass it the project context, the user request, AND the full plan from step 1.

3. Use the `reviewer` agent to review the code.
   Pass it the project context, the user request, the plan, AND the code from step 2.

4. If the reviewer says REVISION NEEDED, send the code back to the `coder` agent
   with the reviewer's feedback. Then run the `reviewer` again.
   Repeat at most 2 times total.

5. When approved (or after 2 revision attempts), print a final summary:
   - Whether the code was approved
   - The key files that were changed
   - The final code output

Coordinate all agents and present the final result clearly.
"""

    async for message in query(
        prompt=conductor_prompt,
        options=ClaudeAgentOptions(
            cwd="c:/Users/ath/FamilieOpskrifter",
            allowed_tools=["Agent"],
            agents={
                "planner": AgentDefinition(
                    description="Plans implementation but never writes code. Given a request and project context, returns a structured plan with files to touch and numbered steps.",
                    prompt=PLANNER_PROMPT,
                    tools=[],
                ),
                "coder": AgentDefinition(
                    description="Implements a given plan. Given a task, plan, and project context, returns complete file contents for all changed files.",
                    prompt=CODER_PROMPT,
                    tools=["Read", "Glob", "Grep"],
                ),
                "reviewer": AgentDefinition(
                    description="Reviews code against a plan. Returns APPROVED or REVISION NEEDED with specific issues listed.",
                    prompt=REVIEWER_PROMPT,
                    tools=["Read"],
                ),
            },
        ),
    ):
        if isinstance(message, ResultMessage):
            print("\n" + "=" * 60)
            print("[Conductor] Pipeline complete.")
            print("=" * 60)
            print(message.result)
