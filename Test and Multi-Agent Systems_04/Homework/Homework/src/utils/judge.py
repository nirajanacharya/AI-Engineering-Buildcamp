"""LLM-based evaluation of agent performance"""
from pydantic import BaseModel
from pydantic_ai import Agent


class EvaluationResult(BaseModel):
    """Result of evaluating agent performance against criteria"""
    passed: bool
    score: float  
    explanation: str


async def evaluate_agent_performance(
    agent_output: str,
    criteria: list[str],
    model: str = "gpt-4o-mini"
) -> EvaluationResult:
    """Evaluate agent output against criteria using an LLM judge
    
    Args:
        agent_output: The agent's text response
        criteria: List of evaluation criteria
        model: LLM model to use for evaluation
        
    Returns:
        EvaluationResult with pass/fail and score
    """
    judge_prompt = f"""Evaluate the following agent output against these criteria:

AGENT OUTPUT:
{agent_output}

CRITERIA:
"""
    for i, criterion in enumerate(criteria, 1):
        judge_prompt += f"{i}. {criterion}\n"
    
    judge_prompt += """
Please evaluate if the output satisfies all criteria. Return a JSON response with:
- passed: boolean (true if all criteria met)
- score: float 0-1 (overall quality score)
- explanation: string (brief explanation of evaluation)
"""
    
    judge_agent = Agent(model=model)
    result = await judge_agent.run(judge_prompt, result_type=EvaluationResult)
    return result.output


async def assert_criteria(
    agent_output: str,
    criteria: list[str],
    model: str = "gpt-4o-mini"
) -> None:
    """Assert that agent output meets all criteria using an LLM judge
    
    Args:
        agent_output: The agent's text response
        criteria: List of evaluation criteria
        model: LLM model to use for evaluation
        
    Raises:
        AssertionError if criteria not met
    """
    result = await evaluate_agent_performance(agent_output, criteria, model)
    assert result.passed, f"Criteria not met: {result.explanation}"
