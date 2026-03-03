# Query for trace IDs
from .client import get_client

def get_trace_ids():
    client = get_client()
    query = '''
    SELECT DISTINCT trace_id
    FROM records
    WHERE span_name = 'trivia_session'
    '''
    result = client.query_json(sql=query)
    return [row['trace_id'] for row in result]

def get_sessions():
    client = get_client()
    query = '''
    SELECT 
        trace_id,
        start_timestamp,
        span_id
    FROM records
    WHERE span_name = 'trivia_session'
    ORDER BY start_timestamp DESC
    '''
    return client.query_json(sql=query)
