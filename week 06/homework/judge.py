from src.evaluation import run_judge_on_results


if __name__ == "__main__":
    rows = run_judge_on_results()
    print(f"\nSaved judged results to results_judged.json")
    print(f"Total judged rows: {len(rows)}")
