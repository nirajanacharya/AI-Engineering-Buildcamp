from minsearch import Index

from .data import load_recipes

RECIPES = load_recipes()

index = Index(
    text_fields=["name", "cuisine", "instructions", "tags_text", "ingredients_text"],
    keyword_fields=["id", "difficulty", "cuisine"],
)

_documents = []
for recipe in RECIPES:
    doc = dict(recipe)
    doc["tags_text"] = ", ".join(recipe["tags"])
    doc["ingredients_text"] = ", ".join(recipe["ingredients"])
    _documents.append(doc)

index.fit(_documents)


def search_recipes(query: str, cuisine: str | None = None) -> str:
    filter_dict = {}
    if cuisine:
        filter_dict["cuisine"] = cuisine

    results = index.search(query, filter_dict=filter_dict, num_results=3)
    if not results:
        return "No recipes found matching your search."

    lines: list[str] = []
    for row in results:
        lines.append(f"[{row['id']}] {row['name']} ({row['cuisine']}, {row['difficulty']})")
        lines.append(
            f"  Prep: {row['prep_time']}min, Cook: {row['cook_time']}min, Serves: {row['servings']}"
        )
        lines.append(f"  Ingredients: {row['ingredients_text']}")
        lines.append(f"  Tags: {row['tags_text']}")
        lines.append("")

    return "\n".join(lines)


def get_recipe(recipe_id: int) -> str:
    for recipe in RECIPES:
        if recipe["id"] == recipe_id:
            ingredients = "\n".join(f"- {item}" for item in recipe["ingredients"])
            return (
                f"Recipe: {recipe['name']}\n"
                f"Cuisine: {recipe['cuisine']}\n"
                f"Difficulty: {recipe['difficulty']}\n"
                f"Prep time: {recipe['prep_time']} minutes\n"
                f"Cook time: {recipe['cook_time']} minutes\n"
                f"Servings: {recipe['servings']}\n\n"
                f"Ingredients:\n{ingredients}\n\n"
                f"Instructions:\n{recipe['instructions']}\n\n"
                f"Tags: {', '.join(recipe['tags'])}"
            )

    return f"Recipe with ID {recipe_id} not found."
