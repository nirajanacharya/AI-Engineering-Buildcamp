# Add feedback to session
import logfire
from src.agent.session import run_session
from src.feedback import ask_feedback

def run_with_feedback(agent, prompt):
    with logfire.span('trivia_session'):
        messages = run_session(agent, prompt)
        feedback = ask_feedback()
        print(f"\nThanks for the feedback: {feedback}")
        return messages
