from src.data import judged_results_path, recipes_path, results_path, scenarios_path


def test_core_data_paths_exist_or_match_expected_files():
    assert recipes_path().name == "recipes.json"
    assert scenarios_path().name == "scenarios.csv"
    assert results_path().name == "results.json"
    assert judged_results_path().name == "results_judged.json"
