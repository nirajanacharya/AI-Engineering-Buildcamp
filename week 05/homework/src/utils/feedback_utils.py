"""Utility functions for collecting and querying user feedback"""

import os
import questionary
from logfire.query_client import LogfireQueryClient


def ask_feedback():
    """Ask the user for feedback on the trivia session.
    
    Returns:
        int or None: 1 for positive, -1 for negative, None for skip
    """
    result = questionary.select(
        "How was the trivia session?",
        choices=["👍 Good", "👎 Bad", "Skip"],
    ).ask()

    if result is None or result == "Skip":
        return None

    return 1 if "Good" in result else -1


def query_feedback(limit: int = 20):
    """Query Logfire to get feedback statistics.
    
    Args:
        limit: Maximum number of feedback records to retrieve
        
    Returns:
        dict: Statistics with 'positive', 'negative', 'total', 'satisfaction_rate'
    """
    read_token = os.getenv('LOGFIRE_READ_TOKEN')
    if not read_token:
        print("⚠ LOGFIRE_READ_TOKEN environment variable not set")
        return None
    
    client = LogfireQueryClient(read_token=read_token)
    
    # Query for all feedback events
    query = f"""
    SELECT 
        trace_id,
        attributes['feedback_score'] as feedback_score,
        attributes['feedback_type'] as feedback_type,
        message,
        start_timestamp
    FROM records
    WHERE message LIKE '%feedback%'
    AND attributes['feedback_score'] IS NOT NULL
    ORDER BY start_timestamp DESC
    LIMIT {limit}
    """
    
    result = client.query_json(query)
    
    positive = 0
    negative = 0
    
    for row in result:
        score = row.get('feedback_score')
        if score == 1:
            positive += 1
        elif score == -1:
            negative += 1
    
    total = positive + negative
    satisfaction_rate = (positive / total * 100) if total > 0 else 0
    
    stats = {
        'positive': positive,
        'negative': negative,
        'total': total,
        'satisfaction_rate': satisfaction_rate,
        'records': result
    }
    
    return stats
