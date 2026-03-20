from types import SimpleNamespace

from src.pricing import calculate_cost


def test_calculate_cost_returns_expected_value():
    usage = SimpleNamespace(input_tokens=1000, output_tokens=500, total_tokens=1500)
    cost = calculate_cost(usage)
    assert cost == 0.00045
