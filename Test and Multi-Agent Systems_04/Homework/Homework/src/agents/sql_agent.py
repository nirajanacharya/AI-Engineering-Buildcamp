import asyncio
from pydantic import BaseModel
from pydantic_ai import Agent
from src.tools.sql_tools import SQLTools


class SQLResult(BaseModel):
    """Result from SQL query execution"""
    sql_query: str
    result_text: str
    row_count: int


async def main():
    
    sql_tools = SQLTools("data/taxi.db")
    
    
    SYSTEM_PROMPT = """
You are a SQL Agent for NYC Taxi dataset.

IMPORTANT: The table name is "trips" - NOT "taxi_rides" or any other name.

Rules:
1. Always call get_schema FIRST to see available columns.
2. The table is named "trips" - always use this name in queries.
3. Generate correct SQL using only available columns from the schema.
4. Return structured JSON:
   - sql_query: the SQL query you ran
   - result_text: the query results
   - row_count: number of rows returned
"""

    
    agent = Agent(
        model="gpt-4o-mini",
        output_type=SQLResult,
        tools=[sql_tools.get_schema, sql_tools.run_sql],
        system_prompt=SYSTEM_PROMPT,
    )

   
    print("Running query: What's the average trip distance for rides with 2 passengers?")
    result = await agent.run("What's the average trip distance for rides with 2 passengers?")
    
    
    print("\n=== RESULTS ===")
    print(f"SQL Query: {result.output.sql_query}")
    print(f"\nResult:\n{result.output.result_text}")
    print(f"Row Count: {result.output.row_count}")


if __name__ == "__main__":
    asyncio.run(main())
