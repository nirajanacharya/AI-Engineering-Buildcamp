"""Utility functions for querying Logfire traces"""

import os
from logfire.query_client import LogfireQueryClient


def get_query_client():
    """Get a Logfire query client with read token from environment.
    
    Returns:
        LogfireQueryClient: Configured query client
        
    Raises:
        ValueError: If LOGFIRE_READ_TOKEN is not set
    """
    read_token = os.getenv('LOGFIRE_READ_TOKEN')
    if not read_token:
        raise ValueError("LOGFIRE_READ_TOKEN environment variable not set")
    
    return LogfireQueryClient(read_token=read_token)


def get_trace_ids(limit: int = 20):
    """Get all recent trace IDs from Logfire.
    
    Args:
        limit: Maximum number of trace IDs to return
        
    Returns:
        list: List of trace ID records
    """
    client = get_query_client()
    
    query = f"""
    SELECT DISTINCT trace_id, start_timestamp
    FROM records
    ORDER BY start_timestamp DESC
    LIMIT {limit}
    """
    
    return client.query_json(query)


def get_trivia_sessions(limit: int = 10):
    """Get trace IDs for trivia sessions (with grouping span).
    
    Args:
        limit: Maximum number of sessions to return
        
    Returns:
        list: List of trivia session records
    """
    client = get_query_client()
    
    query = f"""
    SELECT DISTINCT trace_id, span_name, start_timestamp
    FROM records
    WHERE span_name = 'trivia_session'
    ORDER BY start_timestamp DESC
    LIMIT {limit}
    """
    
    return client.query_json(query)


def get_token_usage(trace_id: str):
    """Get token usage for a specific trace.
    
    Args:
        trace_id: The trace ID to query
        
    Returns:
        dict: Dictionary with 'input_tokens' and 'output_tokens'
    """
    client = get_query_client()
    
    query = f"""
    SELECT 
        SUM(CAST(attributes['llm.usage.prompt_tokens'] AS INTEGER)) as input_tokens,
        SUM(CAST(attributes['llm.usage.completion_tokens'] AS INTEGER)) as output_tokens
    FROM records
    WHERE trace_id = '{trace_id}'
    AND attributes['llm.usage.prompt_tokens'] IS NOT NULL
    """
    
    result = client.query_json(query)
    
    if result and len(result) > 0:
        row = result[0]
        return {
            'input_tokens': row.get('input_tokens', 0) or 0,
            'output_tokens': row.get('output_tokens', 0) or 0
        }
    
    return {'input_tokens': 0, 'output_tokens': 0}


def get_trace_details(trace_id: str):
    """Get detailed information for a specific trace.
    
    Args:
        trace_id: The trace ID to query
        
    Returns:
        list: List of span records for the trace
    """
    client = get_query_client()
    
    query = f"""
    SELECT span_name, message, start_timestamp, attributes
    FROM records
    WHERE trace_id = '{trace_id}'
    ORDER BY start_timestamp
    """
    
    return client.query_json(query)
