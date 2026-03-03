# Quick tests for the modules
import pytest
import os
from src.tools import TriviaTools
from src.agent import create_agent
from src.pricing import calculate_cost


def test_get_categories():
    tools = TriviaTools()
    categories = tools.get_categories()
    
    assert isinstance(categories, str)
    assert len(categories.split('\n')) >= 20


def test_get_questions():
    tools = TriviaTools()
    questions = tools.get_questions(amount=2, category=17, difficulty="easy")
    
    assert isinstance(questions, str)
    assert "Q1:" in questions


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OPENAI_API_KEY")
def test_create_agent():
    agent = create_agent()
    assert agent is not None


def test_calculate_cost():
    cost = calculate_cost("gpt-4o-mini", 1000, 500)
    assert cost > 0
    assert cost < 1


def test_invalid_model():
    with pytest.raises(ValueError):
        calculate_cost("invalid-model", 100, 100)

        
        # Expected: (1000/1M * 0.15) + (500/1M * 0.60)
        expected = (1000 / 1_000_000 * 0.15) + (500 / 1_000_000 * 0.60)
        
        assert abs(cost - expected) < 0.0001
    
    def test_calculate_cost_invalid_model(self):
        """Test cost calculation with invalid model"""
        with pytest.raises(ValueError):
            calculate_cost("invalid-model", 1000, 500)
