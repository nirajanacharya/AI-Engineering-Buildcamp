# Just fetch data from trivia API
import requests

def fetch_categories():
    url = "https://opentdb.com/api_category.php"
    return requests.get(url).json()

def fetch_questions(amount, category, difficulty):
    params = {
        'amount': amount,
        'category': category,
        'difficulty': difficulty,
        'type': 'multiple'
    }
    url = "https://opentdb.com/api.php"
    return requests.get(url, params=params).json()
