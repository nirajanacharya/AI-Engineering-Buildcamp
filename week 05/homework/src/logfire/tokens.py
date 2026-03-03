# Get token usage from logfire
from .client import get_client

def get_token_usage(trace_id):
    client = get_client()
    query = f'''
    SELECT 
        SUM(attributes['llm.usage.input_tokens']) as input_tokens,
        SUM(attributes['llm.usage.output_tokens']) as output_tokens
    FROM records
    WHERE trace_id = '{trace_id}'
    AND attributes['llm.usage.input_tokens'] IS NOT NULL
    '''
    result = client.query_json(sql=query)
    if result:
        return {
            'input': int(result[0]['input_tokens'] or 0),
            'output': int(result[0]['output_tokens'] or 0)
        }
    return {'input': 0, 'output': 0}
