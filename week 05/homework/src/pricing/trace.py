# Combine token usage + cost calculation
from src.logfire import get_token_usage
from src.pricing import calculate_cost

def get_trace_cost(trace_id, model="gpt-4o-mini"):
    usage = get_token_usage(trace_id)
    return calculate_cost(model, usage['input'], usage['output'])
