from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
OUTPUT_PATH = ROOT / "data" / "recipes.json"
OUTPUT_JS_PATH = ROOT / "data" / "recipes.js"
ALLOWED_CATEGORIES = ("dinner", "desserts", "cakes", "uncategorized")
IMAGE_PREFERENCE = ("image.png", "image.jpg", "image.jpeg", "image.webp")


@dataclass
class Recipe:
    id: str
    slug: str
    category: str
    title: str
    description: str
    servings: str
    time: str
    ingredients: list[str]
    method: list[str]
    notes: list[str]
    image: str
    source_txt: str


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").strip().title()


def find_image(recipe_dir: Path) -> Path | None:
    for filename in IMAGE_PREFERENCE:
        candidate = recipe_dir / filename
        if candidate.exists():
            return candidate
    return None


def parse_recipe_file(recipe_txt: Path, slug: str) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    parsed = {
        "title": "",
        "description": "",
        "servings": "",
        "time": "",
        "ingredients": [],
        "method": [],
        "notes": [],
    }

    current_section = None
    # utf-8-sig tolerates UTF-8 files with BOM written by some editors.
    lines = recipe_txt.read_text(encoding="utf-8-sig").splitlines()
    required_headers_seen = set()

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        if line.startswith("TITLE:"):
            parsed["title"] = line.split(":", 1)[1].strip()
            required_headers_seen.add("TITLE")
            current_section = None
            continue
        if line.startswith("DESCRIPTION:"):
            parsed["description"] = line.split(":", 1)[1].strip()
            required_headers_seen.add("DESCRIPTION")
            current_section = None
            continue
        if line.startswith("SERVINGS:"):
            parsed["servings"] = line.split(":", 1)[1].strip()
            required_headers_seen.add("SERVINGS")
            current_section = None
            continue
        if line.startswith("TIME:"):
            parsed["time"] = line.split(":", 1)[1].strip()
            required_headers_seen.add("TIME")
            current_section = None
            continue
        if line.startswith("INGREDIENTS:"):
            required_headers_seen.add("INGREDIENTS")
            current_section = "ingredients"
            continue
        if line.startswith("METHOD:"):
            required_headers_seen.add("METHOD")
            current_section = "method"
            continue
        if line.startswith("NOTER:"):
            current_section = "notes"
            continue

        if current_section == "ingredients":
            if line.startswith("- "):
                parsed["ingredients"].append(line[2:].strip())
            else:
                warnings.append(f"{recipe_txt}: ingredient line should start with '- ': {line}")
                parsed["ingredients"].append(line)
            continue

        if current_section == "method":
            cleaned = re.sub(r"^\d+\.\s*", "", line).strip()
            parsed["method"].append(cleaned if cleaned else line)
            continue

        if current_section == "notes":
            cleaned = line[2:].strip() if line.startswith("- ") else line
            parsed["notes"].append(cleaned)
            continue

    missing_headers = [h for h in ("TITLE", "DESCRIPTION", "SERVINGS", "TIME", "INGREDIENTS", "METHOD") if h not in required_headers_seen]
    if missing_headers:
        warnings.append(f"{recipe_txt}: missing headers: {', '.join(missing_headers)}")

    if not parsed["title"]:
        parsed["title"] = slug_to_title(slug)
        warnings.append(f"{recipe_txt}: TITLE missing/empty, using '{parsed['title']}'")

    if not parsed["description"]:
        parsed["description"] = "Beskrivelse mangler."
        warnings.append(f"{recipe_txt}: DESCRIPTION missing/empty, using fallback")

    return parsed, warnings


def build() -> int:
    all_warnings: list[str] = []
    recipes: list[Recipe] = []
    seen_ids: set[str] = set()

    if not CONTENT_DIR.exists():
        print(f"ERROR: Content directory does not exist: {CONTENT_DIR}")
        return 1

    for category_dir in sorted(CONTENT_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name.lower()
        if category not in ALLOWED_CATEGORIES:
            if not category.startswith("_"):
                all_warnings.append(f"{category_dir}: unknown category folder, skipped")
            continue

        for recipe_dir in sorted(category_dir.iterdir()):
            if not recipe_dir.is_dir():
                continue

            slug = recipe_dir.name
            recipe_txt = recipe_dir / "recipe.txt"
            if not recipe_txt.exists():
                all_warnings.append(f"{recipe_dir}: missing recipe.txt, skipped")
                continue

            image_path = find_image(recipe_dir)
            if image_path is None:
                all_warnings.append(f"{recipe_dir}: missing image file (expected one of: {', '.join(IMAGE_PREFERENCE)}), skipped")
                continue

            recipe_id = f"{category}/{slug}"
            if recipe_id in seen_ids:
                print(f"ERROR: duplicate recipe id: {recipe_id}")
                return 1
            seen_ids.add(recipe_id)

            parsed, parse_warnings = parse_recipe_file(recipe_txt, slug)
            all_warnings.extend(parse_warnings)

            image_rel = image_path.relative_to(ROOT).as_posix()
            txt_rel = recipe_txt.relative_to(ROOT).as_posix()

            recipes.append(
                Recipe(
                    id=recipe_id,
                    slug=slug,
                    category=category,
                    title=parsed["title"],
                    description=parsed["description"],
                    servings=parsed["servings"],
                    time=parsed["time"],
                    ingredients=parsed["ingredients"],
                    method=parsed["method"],
                    notes=parsed["notes"],
                    image=f"./{image_rel}",
                    source_txt=f"./{txt_rel}",
                )
            )

    recipes.sort(key=lambda r: (ALLOWED_CATEGORIES.index(r.category), r.title.lower()))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps([asdict(recipe) for recipe in recipes], ensure_ascii=False, indent=2)
    OUTPUT_PATH.write_text(serialized + "\n", encoding="utf-8")
    OUTPUT_JS_PATH.write_text(f"window.__RECIPES__ = {serialized};\n", encoding="utf-8")

    print(f"Wrote {len(recipes)} recipes to {OUTPUT_PATH}")
    print(f"Wrote script fallback to {OUTPUT_JS_PATH}")
    if all_warnings:
        print("\nWarnings:")
        for warning in all_warnings:
            print(f"- {warning}")

    return 0


if __name__ == "__main__":
    raise SystemExit(build())
