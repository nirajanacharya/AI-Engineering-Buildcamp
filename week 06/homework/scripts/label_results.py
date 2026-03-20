import csv
import json
from pathlib import Path

from src.data import human_labels_path, results_path


def load_existing(path: Path):
    if not path.exists():
        return {}
    with path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    return {row['question']: row for row in rows}


def main():
    results_file = results_path()
    labels_path = human_labels_path()

    if not results_file.exists():
        print('results.json not found. Run: uv run python run_scenarios.py')
        return

    with results_file.open(encoding='utf-8') as f:
        results = json.load(f)

    existing = load_existing(labels_path)

    for i, row in enumerate(results, start=1):
        q = row['question']
        if q in existing and existing[q].get('label') in {'good', 'bad'}:
            continue

        print(f"\n[{i}/{len(results)}] Question: {q}")
        print('Response:')
        print(row['output'])
        print('\nLabel options: good / bad / skip / quit')

        while True:
            label = input('Label: ').strip().lower()
            if label in {'good', 'bad', 'skip', 'quit'}:
                break
            print('Please type good, bad, skip, or quit')

        if label == 'quit':
            break
        if label == 'skip':
            continue

        reason = input('Reason (short): ').strip()
        existing[q] = {'question': q, 'label': label, 'reason': reason}

    rows = list(existing.values())
    rows.sort(key=lambda x: x['question'])

    with labels_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['question', 'label', 'reason'])
        writer.writeheader()
        writer.writerows(rows)

    print(f'Saved {len(rows)} labels to {labels_path}')


if __name__ == '__main__':
    main()
