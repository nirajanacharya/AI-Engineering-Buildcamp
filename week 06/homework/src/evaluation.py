import time

from .assistant import agent
from .data import judged_results_path, load_results, load_scenarios, save_results
from .judge import build_judge
from .pricing import calculate_cost


def run_scenarios() -> list[dict]:
    scenarios = load_scenarios()
    rows: list[dict] = []

    for i, scenario in enumerate(scenarios):
        question = scenario["question"]
        print(f"[{i+1}/{len(scenarios)}] {question}")

        start = time.time()
        result = agent.run_sync(question)
        elapsed = time.time() - start

        usage = result.usage()
        cost = calculate_cost(usage)

        rows.append(
            {
                "question": question,
                "category": scenario["category"],
                "type": scenario["type"],
                "output": result.output,
                "execution_time": round(elapsed, 2),
                "tokens": {
                    "input_tokens": usage.input_tokens,
                    "output_tokens": usage.output_tokens,
                    "total_tokens": usage.total_tokens,
                },
                "cost": cost,
            }
        )
        print(f"  Done in {elapsed:.1f}s (${cost})")

    save_results(rows)
    return rows


def run_judge_on_results() -> list[dict]:
    results = load_results()
    judge_agent = build_judge()

    for i, row in enumerate(results):
        prompt = f"Question: {row['question']}\nAgent response: {row['output']}"
        evaluation = judge_agent.run_sync(prompt)
        row["judge_label"] = evaluation.output.label
        row["judge_reasoning"] = evaluation.output.reasoning
        print(f"[{i+1}/{len(results)}] {row['judge_label']}: {row['question']}")

    save_results(results, path=judged_results_path())
    return results
