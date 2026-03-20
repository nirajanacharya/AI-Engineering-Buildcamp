from typing import Literal

from pydantic import BaseModel
from pydantic_ai import Agent

from .config import load_env

load_env()


class JudgeEvaluation(BaseModel):
    reasoning: str
    label: Literal["good", "bad"]


JUDGE_INSTRUCTIONS = """You are an expert evaluator assessing a recipe assistant that answers
cooking questions using a fixed recipe collection.

A response is \"good\" if:
1. It accurately answers using ONLY information from the recipe collection
2. It correctly identifies when a recipe is not available and says so
3. It correctly identifies out-of-scope questions (not about cooking/recipes) and declines

A response is \"bad\" if ANY of these apply:
1. It makes up recipes, ingredients, or instructions not in the collection (hallucination)
2. It provides cooking advice (substitutions, nutrition info, storage tips) that it
   invented rather than found in the recipe data
3. It answers a question it should have declined (not about recipes, or recipe not available)
4. It gives incorrect information from the recipes (wrong times, wrong ingredients, wrong steps)
5. It says it cannot help when a matching recipe exists in the collection

Be strict about hallucination. The assistant should only provide information it found
in the recipe data. General cooking knowledge that goes beyond the recipe text counts
as hallucination.
"""


def build_judge(model: str = "openai:gpt-4o-mini") -> Agent:
    return Agent(model, output_type=JudgeEvaluation, instructions=JUDGE_INSTRUCTIONS)
