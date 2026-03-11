# Project Overview — FamilieOpskrifter

A static family recipe website with no server, no framework, and no build step beyond the Python data generator.

## Tech stack
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Single `styles.css` file
- **Data pipeline**: Python 3 (`scripts/build_recipes.py`)
- **Hosting**: Static files, open via `OPEN_WEBSITE.cmd` or a local server

## Key files
| File | Purpose |
|------|---------|
| `index.html` | Recipe browser — search, filter by category, card grid |
| `recipe.html` | Recipe detail page — loaded via `?id=category/slug` |
| `wheel.html` | Recipe roulette spin wheel |
| `styles.css` | All styling for all pages |
| `scripts/build_recipes.py` | Scans `content/`, generates `data/recipes.json` and `data/recipes.js` |
| `data/recipes.json` | Generated recipe data (source of truth at runtime) |
| `data/recipes.js` | Same data as a JS fallback (`window.__RECIPES__`) |

## Directory structure
```
content/
  <category>/          # dinner, desserts, cakes, uncategorized
    <recipe-slug>/
      recipe.txt       # recipe data in custom text format
      image.png        # (or .jpg/.jpeg/.webp)

data/
  recipes.json         # generated
  recipes.js           # generated

scripts/
  build_recipes.py     # data generator
  agents/              # AI agent system

brain/                 # project documentation (you are here)
.claude/
  settings.json        # Claude Code settings
  agents/              # agent role definitions
CLAUDE.md              # Orchestrator instructions
```

## Conventions
- No npm, no bundler, no TypeScript
- Python 3 only for tooling
- All CSS in one file
- Recipe categories are fixed: `dinner`, `desserts`, `cakes`, `uncategorized`
