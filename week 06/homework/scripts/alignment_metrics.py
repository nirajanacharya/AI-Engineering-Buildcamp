import json
import csv

from src.data import human_labels_path, judged_results_path


def load_human_labels(path=None):
    if path is None:
        path = human_labels_path()
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    return {row['question']: row['label'].strip().lower() for row in rows if row.get('question') and row.get('label')}


def main():
    with open(judged_results_path(), encoding='utf-8') as f:
        judged = json.load(f)

    human = load_human_labels()

    paired = [row for row in judged if row['question'] in human]
    if not paired:
        print('No overlap between results_judged.json and human_labels.csv')
        return

    tp = fp = fn = tn = 0

    for row in paired:
        judge_bad = row.get('judge_label') == 'bad'
        human_bad = human[row['question']] == 'bad'

        if judge_bad and human_bad:
            tp += 1
        elif judge_bad and not human_bad:
            fp += 1
        elif not judge_bad and human_bad:
            fn += 1
        else:
            tn += 1

    total = len(paired)
    accuracy = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0

    print(f'Total paired rows: {total}')
    print(f'TP={tp}, FP={fp}, FN={fn}, TN={tn}')
    print(f'accuracy={accuracy:.4f}')
    print(f'precision={precision:.4f}')
    print(f'recall={recall:.4f}')

    almond = [
        row for row in paired
        if 'almond milk' in row['question'].lower() and 'pancake' in row['question'].lower()
    ]

    if almond:
        row = almond[0]
        human_label = human[row['question']]
        judge_label = row.get('judge_label')
        agree = 'yes' if human_label == judge_label else 'no'
        print('\nAlmond milk scenario:')
        print(f"human_label={human_label}")
        print(f"judge_label={judge_label}")
        print(f"agree={agree}")
        print('judge_reasoning:')
        print(row.get('judge_reasoning', ''))


if __name__ == '__main__':
    main()
