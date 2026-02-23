"""Tests for SQL Agent"""
import pytest
import duckdb
from src.tools.sql_tools import SQLTools
from pydantic_ai import Agent
from pydantic import BaseModel
from src.utils.utils import collect_tools
from src.utils.judge import assert_criteria



DB_FILE = "data/taxi.db"


class SQLResult(BaseModel):
    """Result from SQL query execution"""
    sql_query: str
    result_text: str
    row_count: int


@pytest.fixture
def sql_tools():
    """Create SQL tools instance"""
    return SQLTools(DB_FILE)


@pytest.fixture
def agent(sql_tools):
    """Create SQL agent"""
    SYSTEM_PROMPT_V2 = """You are a SQL Agent for the NYC Yellow Taxi dataset stored in duckdb.

DATABASE SCHEMA:
- Table name: "trips" (this is the ONLY table)
- The table contains NYC taxi trip data from 2024

CRITICAL RULES:
1. ALWAYS start by calling get_schema() to see the exact column names
2. NEVER use table names like 'taxi_rides', 'taxi_data', 'yellow_trips', etc.
3. ALWAYS use the table name "trips" in all SQL queries
4. Only use column names that exist in the schema
5. Generate correct SQL using DuckDB syntax
6. When asked about average, use AVG() function
7. When asked about passengers, look for columns like 'passenger_count' or similar

Return a SQLResult with:
- sql_query: the exact SQL query you ran
- result_text: the query results
- row_count: number of rows returned"""
    
    agent = Agent(
        model="gpt-4o-mini",
        output_type=SQLResult,
        tools=[sql_tools.get_schema, sql_tools.run_sql],
        system_prompt=SYSTEM_PROMPT_V2,
    )
    return agent


@pytest.mark.asyncio
async def test_q3_trips_more_than_5_passengers(agent):
    """Q3: Test that agent correctly counts trips with > 5 passengers
    
    Expected answer: 22,413
    """
    result = await agent.run("How many trips had more than 5 passengers?")
    
    
    assert isinstance(result.output.sql_query, str)
    assert len(result.output.sql_query) > 0
    assert isinstance(result.output.result_text, str)
    assert "22413" in result.output.result_text.replace(",", "")
    
    print(f"✓ Q3 Query: {result.output.sql_query}")
    print(f"✓ Q3 Result: {result.output.result_text}")


@pytest.mark.asyncio
async def test_q4_tool_call_order(agent):
    """Q4: Test that agent calls get_schema first, then run_sql
    
    The first tool should be get_schema, and run_sql should also be called.
    """
    result = await agent.run("What is the most common payment type?")
    
   
    tool_calls = collect_tools(result._all_messages)
    
    
    assert len(tool_calls) > 0, "No tool calls were made"
    assert tool_calls[0] == "get_schema", f"First tool should be get_schema, got {tool_calls[0]}"
    assert "run_sql" in tool_calls, "run_sql should be called"
    
    print(f"✓ Q4 Tool calls in order: {tool_calls}")
    print(f"✓ Q4 Second tool called: {tool_calls[1] if len(tool_calls) > 1 else 'N/A'}")


@pytest.mark.asyncio
async def test_q5_llm_judge_highest_fare_hour(agent):
    """Q5: Test with LLM judge for hour with highest average fare
    
    Criteria:
    - The SQL query correctly calculates average fare by hour of day
    - The result identifies a specific hour as having the highest average fare
    - The result includes the actual average fare amount
    """
    result = await agent.run("Which hour of the day has the highest average fare amount?")
    
    criteria = [
        "The SQL query correctly calculates average fare amount by hour of day",
        "The result identifies a specific hour (0-23) as having the highest average fare",
        "The result includes the actual average fare amount value"
    ]
    
    
    await assert_criteria(result.output.result_text, criteria)
    
    print(f" Q5 Query: {result.output.sql_query}")
    print(f" Q5 Result: {result.output.result_text}")


@pytest.mark.asyncio
async def test_q6_avg_tip_credit_card(agent):
    """Q6: Average tip amount for credit card payments"""
    result = await agent.run("What is the average tip amount for credit card payments?")
    
    assert isinstance(result.output.sql_query, str)
    assert len(result.output.sql_query) > 0
    assert isinstance(result.output.result_text, str)
    assert len(result.output.result_text) > 0
    
    print(f"Q6a Query: {result.output.sql_query}")
    print(f"Q6a Result: {result.output.result_text}")


@pytest.mark.asyncio
async def test_q6_busiest_location(agent):
    """Q6: Which pickup location has the most trips"""
    result = await agent.run("Which pickup location (PULocationID) has the most trips?")
    
    assert isinstance(result.output.sql_query, str)
    assert len(result.output.sql_query) > 0
    assert isinstance(result.output.result_text, str)
    assert len(result.output.result_text) > 0
    
    print(f"Q6b Query: {result.output.sql_query}")
    print(f"Q6b Result: {result.output.result_text}")


@pytest.mark.asyncio
async def test_q6_avg_fare_long_trips(agent):
    """Q6: Average fare for trips longer than 10 miles"""
    result = await agent.run("What is the average fare for trips longer than 10 miles?")
    
    assert isinstance(result.output.sql_query, str)
    assert len(result.output.sql_query) > 0
    assert isinstance(result.output.result_text, str)
    assert len(result.output.result_text) > 0
    
    print(f"Q6c Query: {result.output.sql_query}")
    print(f"Q6c Result: {result.output.result_text}")


@pytest.mark.asyncio
async def test_q6_zero_passengers(agent):
    """Q6: How many trips had zero passengers - tests passenger_count column"""
    result = await agent.run("How many trips had zero passengers recorded?")
    
    assert isinstance(result.output.sql_query, str)
    assert "passenger_count" in result.output.sql_query, \
        "Query should filter on passenger_count column"
    assert len(result.output.result_text) > 0
    
    print(f"Q6d Query: {result.output.sql_query}")
    print(f"Q6d Result: {result.output.result_text}")


@pytest.mark.asyncio
async def test_q6_busiest_day_of_week(agent):
    """Q6: Busiest day of the week for taxi trips"""
    result = await agent.run("What is the busiest day of the week for taxi trips?")
    
    assert isinstance(result.output.sql_query, str)
    assert len(result.output.sql_query) > 0
    assert isinstance(result.output.result_text, str)
    assert len(result.output.result_text) > 0
    
    print(f"Q6e Query: {result.output.sql_query}")
    print(f"Q6e Result: {result.output.result_text}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
