# Trivia tools that combine API fetch + format
from src.api import fetch_categories, fetch_questions, format_categories, format_questions

class TriviaTools:
    def get_categories(self):
        data = fetch_categories()
        return format_categories(data)
    
    def get_questions(self, amount: int, category: int, difficulty: str):
        data = fetch_questions(amount, category, difficulty)
        return format_questions(data)
