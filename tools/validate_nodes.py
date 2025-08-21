import json
import os
from typing import Dict, List, Set


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

FILES = [
    'expanded_dragon_scenario.json',
    'expanded_magical_forest.json',
    'expanded_hive_city.json',
    'expanded_cyberpunk.json',
]


def load_json(path: str) -> Dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_target(choice: Dict) -> str:
    return choice.get('next_node') or choice.get('nextNode') or choice.get('next_node_id') or ''


def validate_file(filename: str) -> List[str]:
    path = os.path.join(DATA_DIR, filename)
    try:
        data = load_json(path)
    except Exception as e:
        return [f"ERROR loading {filename}: {e}"]

    scenarios = data.get('enhanced_scenarios', {})
    if not scenarios:
        return [f"WARN {filename}: no enhanced_scenarios key"]

    report: List[str] = []
    for scenario_id, scenario in scenarios.items():
        nodes: Dict[str, Dict] = scenario.get('nodes', {})
        if not nodes:
            report.append(f"ERROR {filename}::{scenario_id}: no nodes found")
            continue

        node_ids: Set[str] = set(nodes.keys())
        if 'start' not in node_ids:
            report.append(f"ERROR {filename}::{scenario_id}: missing 'start' node")

        missing: Set[str] = set()
        missing_details: List[str] = []
        
        for nid, node in nodes.items():
            for i, choice in enumerate(node.get('choices', [])):
                target = get_target(choice)
                if not target:
                    report.append(f"WARN  {filename}::{scenario_id} node='{nid}' choice[{i}]: '{choice.get('text','')}' has no next_node")
                    continue
                # allow self, start, and existing nodes
                if target not in node_ids and target not in {'start'}:
                    missing.add(target)
                    missing_details.append(f"  - {target} (from {nid} choice[{i}]: '{choice.get('text','')}')")

        if missing:
            report.append(f"MISSING {filename}::{scenario_id}: {len(missing)} targets not found:")
            report.extend(missing_details)
        else:
            report.append(f"OK     {filename}::{scenario_id}: all next_node targets resolve")

    return report


def main():
    any_missing = False
    for f in FILES:
        lines = validate_file(f)
        for line in lines:
            print(line)
            if line.startswith('MISSING') or line.startswith('ERROR'):
                any_missing = True

    if any_missing:
        exit(1)


if __name__ == '__main__':
    main()


