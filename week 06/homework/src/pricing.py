MODEL_PRICES = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}


def calculate_cost(usage, model: str = "gpt-4o-mini") -> float:
    prices = MODEL_PRICES[model]
    input_cost = (usage.input_tokens / 1_000_000) * prices["input"]
    output_cost = (usage.output_tokens / 1_000_000) * prices["output"]
    return round(input_cost + output_cost, 6)
