# Frontend Architecture

All pages are plain HTML files that load `data/recipes.js` as a script tag fallback,
then fetch `data/recipes.json` via `fetch()`.

## Pages

### index.html — Recipe Browser
- Loads all recipes and renders them as cards in a grid
- Features: text search, category filter buttons, responsive grid
- Each card links to `recipe.html?id=<category/slug>`
- Recipe data accessed via `window.__RECIPES__` (from recipes.js) or fetch

### recipe.html — Recipe Detail
- Reads `?id=` query param to find the recipe
- Renders: image, title, description, servings, time, ingredients, method, notes
- Back button returns to index.html

### wheel.html — Recipe Roulette
- Spin wheel that randomly selects a recipe
- Uses canvas or CSS animation
- Links to recipe.html on selection

## Styling
Single file: `styles.css`
- CSS custom properties for colors/spacing
- Mobile-first responsive design
- No external CSS libraries

## Data loading pattern
```js
// Preferred: fetch JSON
fetch('./data/recipes.json')
  .then(r => r.json())
  .then(recipes => render(recipes))

// Fallback: recipes.js sets window.__RECIPES__
// Used when fetch fails (e.g. file:// protocol)
```

## No build step
All JS is inline in the HTML files or in `<script>` tags.
There is no bundler, transpiler, or package.json.
