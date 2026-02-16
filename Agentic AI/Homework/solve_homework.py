import requests
import os
import sys
import asyncio
import traceback
from typing import List, Optional

# Try to load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from pydantic_ai import Agent, RunContext, Tool
from pydantic import BaseModel

# --- Configuration ---
SEARCH_URL = "https://en.wikipedia.org/w/api.php"
PAGE_URL = "https://en.wikipedia.org/w/index.php"
HEADERS = {"User-Agent": "HomeworkSolverAgent/1.0 (learning_project; python-requests)"}

# --- Tools ---

def search_wikipedia(query: str) -> List[dict]:
    """
    Search Wikipedia for a given query.
    """
    print(f"Tool Call: search_wikipedia('{query}')")
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "utf8": 1,
        "formatversion": 2
    }
    try:
        response = requests.get(SEARCH_URL, params=params, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if "query" in data and "search" in data["query"]:
            return data["query"]["search"]
        return []
    except Exception as e:
        with open("debug_error.txt", "w") as f:
            f.write(traceback.format_exc())
        print(f"Error in search_wikipedia: {e}")
        # Return empty list to avoid crashing if possible, or re-raise if critical
        raise

def get_page(title: str) -> str:
    """
    Fetch the raw content of a Wikipedia page.
    """
    print(f"Tool Call: get_page('{title}')")
    params = {
        "action": "raw",
        "title": title
    }
    try:
        response = requests.get(PAGE_URL, params=params, headers=HEADERS)
        if response.status_code == 404:
            return "Page not found."
        response.raise_for_status()
        return response.text
    except Exception as e:
        with open("debug_error.txt", "a") as f:
             f.write(f"\n--- Get Page Error ---\n{traceback.format_exc()}")
        print(f"Error in get_page: {e}")
        raise

# --- Questions ---

def solve_q1():
    print("\n--- Question 1 ---")
    results = search_wikipedia("capybara")
    print(f"Total results returned: {len(results)}")
    return results

def solve_q2(results):
    print("\n--- Question 2 ---")
    count = 0
    for result in results:
        if "capybara" in result["title"].lower():
            count += 1
    print(f"Results with 'capybara' in title: {count}")

def solve_q3():
    print("\n--- Question 3 ---")
    content = get_page("Capybara")
    print(f"Character count in 'Capybara' page: {len(content)}")

def setup_agent():
    print("\n--- Question 4 (Agent Setup) ---")
    model = 'openai:gpt-4o'
    
    agent = Agent(
        model,
        system_prompt="You are a helpful assistant that can answer questions using Wikipedia. Use the search_wikipedia tool to find relevant pages and the get_page tool to read their content."
    )
    
    @agent.tool
    def search_tool(ctx: RunContext, query: str) -> List[dict]:
        return search_wikipedia(query)

    @agent.tool
    def get_page_tool(ctx: RunContext, title: str) -> str:
        return get_page(title)
        
    print(f"Agent setup with model: {model}")
    return agent

async def solve_q5_q6(agent):
    print("\n--- Question 5 ---")
    query_q5 = "What is this page about? https://en.wikipedia.org/wiki/Capybara"
    
    try:
        result_q5 = await agent.run(query_q5)
        print("Agent Answer Q5 (Raw Result):")
        print(result_q5)
        if hasattr(result_q5, 'data'):
            print(result_q5.data)
        elif hasattr(result_q5, 'content'):
            print(result_q5.content)
    except Exception as e:
        print(f"Error in Q5: {e}")

    print("\n--- Question 6 ---")
    query_q6 = "What are the main threats to capybara populations?"
    try:
        # PydanticAI doesn't easily expose 'tool calls count' in the result object directly in a simple property,
        # but we can see it in logs or by wrapping tools.
        # We are printing usage in the tools themselves.
        result_q6 = await agent.run(query_q6)
        print("Agent Answer Q6 (Raw Result):")
        print(result_q6)
        if hasattr(result_q6, 'data'):
            print(result_q6.data)
        elif hasattr(result_q6, 'content'):
            print(result_q6.content)
    except Exception as e:
        print(f"Error in Q6: {e}")

async def main():
    # Check API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("WARNING: OPENAI_API_KEY environment variable not set. Agent questions (Q4-Q6) will fail.")
    else:
        print("OPENAI_API_KEY is set.")

    # Q1 & Q2
    try:
        results = solve_q1()
        solve_q2(results)
    except Exception as e:
        print(f"Failed Q1/Q2: {e}")
        return
    
    # Q3
    try:
        solve_q3()
    except Exception as e:
        print(f"Failed Q3: {e}")
        return
    
    # Q4, Q5, Q6
    if api_key:
        agent = setup_agent()
        await solve_q5_q6(agent)
    else:
        print("\nSkipping Q4-Q6 due to missing API Key.")

if __name__ == "__main__":
    asyncio.run(main())
