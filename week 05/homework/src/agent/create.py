# Create the trivia agent
from pydantic_ai import Agent
from src.tools import TriviaTools
from .prompts import TRIVIA_PROMPT

def create_agent(model="openai:gpt-4o-mini"):
    tools = TriviaTools()
    return Agent(
        model,
        tools=[tools.get_categories, tools.get_questions],
        system_prompt=TRIVIA_PROMPT
    )
