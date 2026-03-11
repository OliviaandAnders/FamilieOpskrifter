# FamilieOpskrifter Agent Team

A native Claude Code agent team for automating changes to the recipe website.

## Architecture

| Role | Defined in | Responsibility |
|------|-----------|---------------|
| **Orchestrator** | `CLAUDE.md` | Team lead — coordinates the pipeline |
| **Researcher** | `.claude/agents/researcher.md` | Reads `brain/` docs and project files, returns context |
| **Planner** | `.claude/agents/planner.md` | Turns request + context into a structured plan (no code) |
| **Coder** | `.claude/agents/coder.md` | Implements the plan, returns complete file contents |
| **Reviewer** | `.claude/agents/reviewer.md` | Approves code or requests revision with specific issues |

## Pipeline
```
User request → Researcher → Planner → Coder → Reviewer
                                          ↑         |
                                          └─ (revision, max 2x)
```

## How to use

1. Make sure agent teams are enabled (already set in `.claude/settings.json`):
   ```
   CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
   ```

2. Open Claude Code in the project root:
   ```
   claude
   ```

3. Tell the Orchestrator to create a team for your task:
   ```
   Create an agent team to add lazy-loading to all recipe images
   ```
   ```
   Create an agent team to add a new "DIFFICULTY" field to recipes
   ```
   ```
   Create an agent team to add a print stylesheet to recipe.html
   ```

4. The Orchestrator (Claude Code lead) will spawn Researcher, Planner, Coder, and Reviewer
   as separate Claude Code instances and coordinate the work.

## Brain folder
`brain/` contains project documentation that the Researcher reads:
- `brain/project-overview.md` — tech stack, file structure
- `brain/recipe-format.md` — recipe.txt field format
- `brain/build-system.md` — how the Python build script works
- `brain/frontend.md` — HTML/JS architecture

Add new docs to `brain/` as the project grows.
