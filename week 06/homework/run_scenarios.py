from src.evaluation import run_scenarios


def run_all():
    results = run_scenarios()
    total_cost = sum(r["cost"] for r in results)
    print(f"\nSaved {len(results)} results to results.json")
    print(f"Total cost: ${total_cost:.4f}")

if __name__ == "__main__":
    run_all()
