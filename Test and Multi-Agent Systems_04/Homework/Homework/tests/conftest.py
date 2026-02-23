"""Pytest configuration and cost tracking for agent tests"""
import pytest
from unittest.mock import patch
from pydantic_ai import Agent



TOTAL_COST = 0.0
CALL_COUNT = 0


def patch_agent():
    """Patch the agent to track API costs
    
    Cost estimates (as of Feb 2026):
    - gpt-4o-mini: $0.15 per 1M input tokens, $0.60 per 1M output tokens
    """
    original_run = Agent.run
    original_run_sync = Agent.run.__wrapped__ if hasattr(Agent.run, '__wrapped__') else None
    
    async def tracked_run(self, *args, **kwargs):
        global TOTAL_COST, CALL_COUNT
        result = await original_run(self, *args, **kwargs)
        
        
        CALL_COUNT += 1
        if "gpt-4" in self.model:
            TOTAL_COST += 0.02  
        else:
            TOTAL_COST += 0.01
        
        return result
    
    Agent.run = tracked_run


@pytest.fixture(scope="session", autouse=True)
def setup_cost_tracking():
    """Setup cost tracking for the entire test session"""
    patch_agent()
    yield
    
   
    print(f"\n\n{'='*60}")
    print(f"COST TRACKING SUMMARY:")
    print(f"Total API Calls: {CALL_COUNT}")
    print(f"Estimated Total Cost: ${TOTAL_COST:.4f}")
    print(f"{'='*60}\n")


@pytest.fixture
def cost_tracker():
    """Provides cost tracking during a test"""
    global TOTAL_COST, CALL_COUNT
    
    start_cost = TOTAL_COST
    start_calls = CALL_COUNT
    
    yield {
        'start_cost': start_cost,
        'start_calls': start_calls
    }
    
    test_cost = TOTAL_COST - start_cost
    test_calls = CALL_COUNT - start_calls
    print(f"\nTest cost: ${test_cost:.4f} ({test_calls} calls)")
