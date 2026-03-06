# Recipe Content Structure

Use this folder structure for each recipe:

content/
  dinner/
    recipe-slug/
      image.png
      recipe.txt
  desserts/
    recipe-slug/
      image.png
      recipe.txt
  cakes/
    recipe-slug/
      image.png
      recipe.txt
  uncategorized/
    recipe-slug/
      image.png
      recipe.txt

Rules:
1. Category is based on the parent folder name (`dinner`, `desserts`, `cakes`, `uncategorized`).
2. One recipe folder per recipe (for example: `chocolate-cake`).
3. Add exactly one main image as `image.png` (or `image.jpg`).
4. Add one text file named `recipe.txt` using the format in `content/_recipe-template.txt`.
5. Keep folder names lowercase and use hyphens (`-`) instead of spaces.
6. Optional: add a `NOTER:` section in `recipe.txt` for extra notes shown on the recipe page.

Example:
content/cakes/chocolate-cake/image.png
content/cakes/chocolate-cake/recipe.txt

Build recipe data for the website:
1. Run `py -3 scripts/build_recipes.py` from the project root.
2. This generates `data/recipes.json` used by `index.html` and `recipe.html`.
3. Deploy the updated files, including `data/recipes.json`.
