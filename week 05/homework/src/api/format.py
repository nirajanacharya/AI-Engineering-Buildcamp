
import html

def format_categories(data):
    result = []
    for cat in data['trivia_categories']:
        result.append(f"{cat['id']}: {cat['name']}")
    return "\n".join(result)

def format_questions(data):
    result = []
    for i, q in enumerate(data['results'], 1):
        question = html.unescape(q['question'])
        correct = html.unescape(q['correct_answer'])
        wrong = [html.unescape(a) for a in q['incorrect_answers']]
        
        result.append(f"Q{i}: {question}")
        result.append(f"Correct: {correct}")
        result.append(f"Wrong: {', '.join(wrong)}\n")
    
    return "\n".join(result)
