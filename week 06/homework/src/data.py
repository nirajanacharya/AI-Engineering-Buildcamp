import csv
import json
from pathlib import Path

from .config import project_root


def _first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def recipes_path() -> Path:
    root = project_root()
    return _first_existing(root / "data" / "raw" / "recipes.json", root / "recipes.json")


def scenarios_path() -> Path:
    root = project_root()
    return _first_existing(root / "data" / "raw" / "scenarios.csv", root / "scenarios.csv")


def results_path() -> Path:
    root = project_root()
    return _first_existing(root / "data" / "outputs" / "results.json", root / "results.json")


def judged_results_path() -> Path:
    root = project_root()
    return _first_existing(
        root / "data" / "outputs" / "results_judged.json", root / "results_judged.json"
    )


def human_labels_path() -> Path:
    root = project_root()
    return _first_existing(root / "data" / "outputs" / "human_labels.csv", root / "human_labels.csv")


def load_recipes() -> list[dict]:
    return json.loads(recipes_path().read_text(encoding="utf-8"))


def load_scenarios() -> list[dict]:
    with scenarios_path().open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_results(path: Path | None = None) -> list[dict]:
    target = path or results_path()
    return json.loads(target.read_text(encoding="utf-8"))


def save_results(rows: list[dict], path: Path | None = None) -> Path:
    target = path or results_path()
    target.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return target
