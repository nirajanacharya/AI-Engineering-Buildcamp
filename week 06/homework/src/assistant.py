from pydantic_ai import Agent

from .config import load_env
from .tools import get_recipe, search_recipes

load_env()

ASSISTANT_INSTRUCTIONS = """You are a recipe assistant. You help users find recipes and answer cooking questions.
1. Use search_recipes to find recipes matching the user's request
2. Use get_recipe to get full details including instructions
3. Answer based on the recipe data you have - do not make up recipes or ingredients
4. If asked about something not in the recipe collection, say you don't have that recipe
5. You can suggest alternatives from the collection if you don't have an exact match
"""


def build_agent(model: str = "openai:gpt-4o-mini") -> Agent:
    return Agent(
        model,
        tools=[search_recipes, get_recipe],
        instructions=ASSISTANT_INSTRUCTIONS,
    )


agent = build_agent()
