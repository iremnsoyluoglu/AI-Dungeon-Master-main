#!/usr/bin/env python3
"""
Fix expanded dragon scenario file
"""

import json
import re

# Read the expanded dragon scenario file
with open('data/expanded_dragon_scenario.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix the structure
if 'enhanced_scenarios' in data and 'dragon_hunters_path' in data['enhanced_scenarios']:
    scenario = data['enhanced_scenarios']['dragon_hunters_path']
    
    # Update the structure to match the new format
    if 'nodes' in scenario:
        scenario['story_nodes'] = scenario.pop('nodes')
    
    # Fix all choices in story_nodes
    if 'story_nodes' in scenario:
        for node_id, node in scenario['story_nodes'].items():
            if 'choices' in node:
                for choice in node['choices']:
                    # Replace stat_effects with effect
                    if 'stat_effects' in choice:
                        stat_effects = choice.pop('stat_effects')
                        # Convert npc_relationship to reputation
                        effect = {}
                        for key, value in stat_effects.items():
                            if key == 'npc_relationship':
                                effect['reputation'] = value
                            else:
                                effect[key] = value
                        choice['effect'] = effect

# Write the fixed data back
with open('data/expanded_dragon_scenario.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Fixed expanded dragon scenario file!")
