
from src.logfire import get_client

def get_feedback_stats():
    client = get_client()
    query = '''
    SELECT 
        attributes['rating'] as rating,
        COUNT(*) as count
    FROM records
    WHERE message = 'user_feedback'
    GROUP BY rating
    ORDER BY count DESC
    '''
    return client.query_json(sql=query)
