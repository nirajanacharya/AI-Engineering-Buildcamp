
import logfire
import questionary

def ask_feedback():
    rating = questionary.select(
        "How was your experience?",
        choices=["Great", "Good", "Okay", "Bad"]
    ).ask()
    
    logfire.info("user_feedback", rating=rating)
    return rating
