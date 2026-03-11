# Build System

## Entry point
```
python scripts/build_recipes.py
```

## What it does
1. Scans `content/` for category folders (`dinner`, `desserts`, `cakes`, `uncategorized`)
2. For each `<category>/<slug>/` folder, reads `recipe.txt` and finds an image file
3. Parses each recipe into a `Recipe` dataclass
4. Sorts recipes: by category order, then alphabetically by title
5. Writes `data/recipes.json` (pretty-printed JSON array)
6. Writes `data/recipes.js` (`window.__RECIPES__ = <json>;`)

## Recipe dataclass fields
```python
@dataclass
class Recipe:
    id: str          # "category/slug"
    slug: str        # folder name
    category: str    # "dinner" | "desserts" | "cakes" | "uncategorized"
    title: str
    description: str
    servings: str
    time: str
    ingredients: list[str]
    method: list[str]
    notes: list[str]
    image: str       # relative path e.g. "./content/dinner/slug/image.png"
    source_txt: str  # relative path to recipe.txt
```

## Image lookup order
`image.png` → `image.jpg` → `image.jpeg` → `image.webp`
If no image is found, the recipe is **skipped** with a warning.

## Adding a new field
1. Add the field to the `Recipe` dataclass in `build_recipes.py`
2. Parse it in `parse_recipe_file()` (see how `TIME:` is handled)
3. The field will automatically appear in `data/recipes.json`
4. Update `index.html` / `recipe.html` JS to read and display it

## Allowed categories
Defined in `ALLOWED_CATEGORIES = ("dinner", "desserts", "cakes", "uncategorized")`.
Unknown folders are skipped with a warning (unless they start with `_`).
