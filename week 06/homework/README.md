# Week 06 Homework - Recipe Assistant Evaluation

This folder is scaffolded for the Buildcamp Week 06 evaluation homework.

## Folder structure

- `src/` modular application code (agent, tools, pricing, evaluation)
- `tests/` unit tests
- `notebooks/` homework notebook
- `data/raw/` static input data (`recipes.json`, `scenarios.csv`)
- `data/outputs/` generated files (`results.json`, `results_judged.json`, `human_labels.csv`)
- `scripts/` CLI utilities (`label_results.py`, `alignment_metrics.py`)

Compatibility wrappers remain at project root:

- `run_scenarios.py`
- `judge.py`
- `label_results.py`
- `alignment_metrics.py`

## Setup

```bash
uv sync
```

Set your OpenAI key:

```bash
# PowerShell
$env:OPENAI_API_KEY="your_key_here"
```

## Run flow

1) Run one quick test

```bash
uv run python -c "from recipe_agent import agent; r = agent.run_sync('How do I make pizza?'); print(r.output)"
```

2) Batch run scenarios

```bash
uv run python run_scenarios.py
```

3) Manually label results

```bash
uv run python label_results.py
```

4) Run judge

```bash
uv run python judge.py
```

5) Compare judge vs human labels

```bash
uv run python alignment_metrics.py
```

Or use `notebooks/homework.ipynb` to compute TP/FP/FN/TN, accuracy, precision, and recall.
