# Calculate costs from token usage
from .rates import PRICES

def calculate_cost(model, input_tokens, output_tokens):
    if model not in PRICES:
        raise ValueError(f"Unknown model: {model}")
    
    prices = PRICES[model]
    input_cost = (input_tokens / 1_000_000) * prices["input"]
    output_cost = (output_tokens / 1_000_000) * prices["output"]
    
    return input_cost + output_cost
