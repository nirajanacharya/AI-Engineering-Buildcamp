"""Utility functions for calculating costs from token usage"""

from src.utils.query_utils import get_token_usage


# Model pricing (per 1M tokens)
MODEL_PRICES = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 5.00, "output": 15.00},
    "gpt-4": {"input": 30.00, "output": 60.00},
}


def calculate_cost(model_name: str, input_tokens: int, output_tokens: int, verbose: bool = False):
    """Calculate the cost of a session given token counts.
    
    Args:
        model_name: Name of the model used
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        verbose: If True, print detailed breakdown
        
    Returns:
        float: Total cost in USD
    """
    if model_name.lower() not in MODEL_PRICES:
        raise ValueError(f"Unknown model: {model_name}. Supported: {list(MODEL_PRICES.keys())}")
    
    prices = MODEL_PRICES[model_name.lower()]
    input_cost = (input_tokens / 1_000_000) * prices["input"]
    output_cost = (output_tokens / 1_000_000) * prices["output"]
    total_cost = input_cost + output_cost
    
    if verbose:
        print(f"\n=== Cost Breakdown ===")
        print(f"Model: {model_name}")
        print(f"Input tokens: {input_tokens:,} @ ${prices['input']}/1M = ${input_cost:.6f}")
        print(f"Output tokens: {output_tokens:,} @ ${prices['output']}/1M = ${output_cost:.6f}")
        print(f"Total cost: ${total_cost:.6f}")
    
    return total_cost


def get_trace_cost(trace_id: str, model_name: str = "gpt-4o-mini", verbose: bool = False):
    """Calculate cost for a specific trace from Logfire.
    
    Args:
        trace_id: The trace ID to calculate cost for
        model_name: Name of the model used
        verbose: If True, print detailed breakdown
        
    Returns:
        float: Total cost in USD
    """
    token_data = get_token_usage(trace_id)
    input_tokens = token_data['input_tokens']
    output_tokens = token_data['output_tokens']
    
    if input_tokens == 0 and output_tokens == 0:
        if verbose:
            print("No token data found for this trace")
        return 0.0
    
    return calculate_cost(model_name, input_tokens, output_tokens, verbose=verbose)
