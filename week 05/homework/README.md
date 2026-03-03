# Trivia Quiz Agent - Week 05 Homework

A modular trivia quiz agent powered by PydanticAI and Logfire, with comprehensive monitoring and observability.

## 📁 Project Structure

```
week 05/homework/
├── notebooks/
│   └── trivia_homework.ipynb    # Main homework notebook with all questions
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── trivia_agent.py      # Agent implementation
│   ├── tools/
│   │   ├── __init__.py
│   │   └── trivia_tools.py      # API tools for fetching trivia questions
│   └── utils/
│       ├── __init__.py
│       ├── query_utils.py       # Logfire query utilities
│       ├── cost_utils.py        # Cost calculation utilities
│       └── feedback_utils.py    # User feedback utilities
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_trivia.py           # Unit tests
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── .gitignore
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd "week 05/homework"
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Make sure your `.env` file (in the root AI-Engineering folder) contains:

```env
OPENAI_API_KEY=your-openai-api-key-here
LOGFIRE_READ_TOKEN=your-logfire-read-token-here
```

### 3. Configure Logfire

```bash
logfire auth
```

### 4. Open the Homework Notebook

```bash
jupyter notebook notebooks/trivia_homework.ipynb
```

Or in VS Code, simply open `notebooks/trivia_homework.ipynb`

## 📓 Using the Notebook

The `trivia_homework.ipynb` notebook contains:

- **Setup cells**: Import libraries and load environment variables
- **Preparation**: Test the tools
- **Question 1-6**: Complete solutions with explanations
- **Bonus Question**: Feedback tracking implementation
- **Summary**: All answers in one table
- **Additional Exploration**: Extra examples

**Important:** The notebook uses `python-dotenv` to automatically load your environment variables from the `.env` file.

## 🏗️ Module Architecture

### `src/tools/trivia_tools.py`

Tools for fetching trivia data from Open Trivia Database API:

```python
from src.tools import TriviaTools

tools = TriviaTools()
categories = tools.get_categories()           # Get all categories
questions = tools.get_questions(5, 17, "easy") # Get 5 easy Science questions
```

### `src/agents/trivia_agent.py`

Agent creation and execution functions:

```python
from src.agents import create_agent, run_trivia, run_trivia_with_grouping

agent = create_agent()                        # Create agent
run_trivia("Let's play 3 questions", agent)   # Run without grouping
run_trivia_with_grouping(prompt, agent)       # Run with trace grouping
```

### `src/utils/query_utils.py`

Query Logfire traces:

```python
from src.utils import get_trivia_sessions, get_token_usage

sessions = get_trivia_sessions()              # Get all trivia sessions
tokens = get_token_usage(trace_id)            # Get token usage for a trace
```

### `src/utils/cost_utils.py`

Calculate costs:

```python
from src.utils import calculate_cost, get_trace_cost

cost = calculate_cost("gpt-4o-mini", 6000, 1000)  # Manual calculation
cost = get_trace_cost(trace_id)                    # From Logfire trace
```

### `src/utils/feedback_utils.py`

Collect and query feedback:

```python
from src.utils import ask_feedback, query_feedback

feedback = ask_feedback()                     # Ask user for feedback
stats = query_feedback()                       # Query feedback statistics
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_trivia.py::TestTriviaTools::test_get_categories
```

## 📋 Homework Answers

| Question | Answer |
|----------|--------|
| Q1: First tool called | `get_categories` |
| Q2: Top-level span name | `pydantic_ai.agent` |
| Q3: Number of traces (5 questions) | `6` |
| Q4: Input tokens range | `2,000 - 10,000` |
| Q5: Trace ID | [Your trace ID from Logfire] |
| Q6: Approximate cost | `Less than $0.01` |
| Bonus: Feedback in same trace | By logging inside `logfire.span()` context |

**All answers are explained in detail in the notebook!**

## 🔍 How It Works

### Tool Calling Flow

```
User: "Let's play 3 questions from History"
    ↓
Agent calls get_categories()
    ↓
Agent finds "History" = category 23
    ↓
Agent calls get_questions(3, 23, "medium")
    ↓
Agent formats and asks Question 1
    ↓
User answers
    ↓
Agent evaluates and explains
    ↓
Repeat for all questions
```

### Monitoring with Logfire

```python
# Configure once
logfire.configure()
logfire.instrument_pydantic_ai()

# Group session under one trace
with logfire.span('trivia_session'):
    run_trivia(prompt)
    
    # Feedback is logged in same trace
    feedback = ask_feedback()
    logfire.info("feedback", feedback_score=feedback)
```

### Cost Calculation

```
Cost = (input_tokens / 1M × $0.15) + (output_tokens / 1M × $0.60)

Example (6000 input, 1000 output):
  = (6000/1M × 0.15) + (1000/1M × 0.60)
  = $0.0009 + $0.0006
  = $0.0015
```

## 🎯 Key Learning Objectives

- ✅ Build modular agent systems
- ✅ Implement tool calling with PydanticAI
- ✅ Instrument code with Logfire for observability
- ✅ Group related operations into traces
- ✅ Query observability data with SQL
- ✅ Calculate and optimize costs
- ✅ Track user feedback in production

## 🔧 Troubleshooting

### Environment Variables Not Loading

```python
# Check if .env file is being loaded
from dotenv import load_dotenv
import os

load_dotenv('path/to/.env')
print(os.getenv('OPENAI_API_KEY'))  # Should not be None
```

### Import Errors

```python
# Make sure you're in the right directory and src is in path
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from src.tools import TriviaTools  # Should work now
```

### Logfire Queries Failing

- Check `LOGFIRE_READ_TOKEN` is set correctly
- Verify you've run the agent at least once
- Check internet connection
- Ensure Logfire project is active

## 📚 API Reference

### Open Trivia Database

- **Base URL**: https://opentdb.com/api.php
- **Categories**: 24 available (General, Science, History, etc.)
- **Difficulties**: easy, medium, hard
- **Free to use, no authentication required**

### Popular Categories

- 9: General Knowledge
- 17: Science & Nature
- 18: Science: Computers
- 21: Sports
- 23: History

## 🎨 Extending This Project

Ideas for enhancement:

1. **Difficulty Progression**: Start easy, increase difficulty
2. **User Statistics**: Track performance over time
3. **Timed Challenges**: Add countdown timers
4. **Team Mode**: Multiple players competing
5. **Leaderboards**: Global or local rankings
6. **Personalized Recommendations**: Based on user preferences
7. **A/B Testing**: Test different explanation styles

## 📊 Logfire Dashboard

Access your dashboard at: https://logfire.pydantic.dev/

View:
- Traces for each agent run
- Token usage and costs
- Tool calls and results
- Performance metrics
- User feedback events

## 📝 Notes

- The notebook is designed to be run cell-by-cell
- Some cells require interactive input (marked with comments)
- All environment variables are loaded from `.env` automatically
- Token counts and costs will vary based on your specific sessions
- Trace IDs are unique for each run

## 🤝 Contributing

This is homework/educational code. Feel free to:
- Modify for learning purposes
- Experiment with different configurations
- Add your own features
- Share improvements with classmates

## 📖 Resources

- [Open Trivia Database](https://opentdb.com/)
- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [Logfire Documentation](https://docs.pydantic.dev/logfire/)
- [Python dotenv](https://pypi.org/project/python-dotenv/)

## ✅ Homework Checklist

- [x] Install dependencies
- [x] Set up environment variables
- [x] Configure Logfire
- [x] Test tools (Preparation)
- [x] Question 1: Identify first tool call
- [x] Question 2: Find top-level span name
- [x] Question 3: Count separate traces
- [x] Question 4: Measure input tokens with grouping
- [x] Question 5: Query trace IDs with SQL
- [x] Question 6: Calculate session cost
- [x] Bonus: Implement feedback tracking

---

**Created for AI Engineering Bootcamp - Week 05**

*A modular, production-ready trivia agent with comprehensive monitoring and observability.*
