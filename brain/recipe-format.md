# Recipe File Format

Each recipe lives in `content/<category>/<slug>/recipe.txt`.

## Fields

```
TITLE: Example Dish
DESCRIPTION: A short description shown on the recipe card.
SERVINGS: 4
TIME: 45 min

INGREDIENTS:
- 500 g ingredient one
- 2 spsk ingredient two
- 1 tsk spice

METHOD:
1. First step of the method.
2. Second step.
3. Third step.

NOTER:
- Optional tip or note.
- Another note.
```

## Rules
- `TITLE`, `DESCRIPTION`, `SERVINGS`, `TIME`, `INGREDIENTS`, `METHOD` are **required**
- `NOTER` is optional
- Ingredient lines must start with `- `
- Method lines are numbered (`1.`, `2.`, ...) — the build script strips the numbers
- Notes lines should start with `- ` (not enforced but expected)
- File encoding: UTF-8 (BOM-tolerant)
- Blank lines are ignored by the parser

## Build warnings
The build script emits warnings for:
- Missing required headers
- Ingredient lines not starting with `- `
- Empty TITLE or DESCRIPTION (uses fallbacks)
- Missing image file (recipe is skipped entirely)

## Template
See `content/_recipe-template.txt` for a blank template.
