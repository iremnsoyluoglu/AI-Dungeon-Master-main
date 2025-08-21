#!/usr/bin/env python3
"""
Debug script to test data loading
"""

import json
import os

def load_json_data(filename):
    try:
        with open(f'data/{filename}', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return {}

# Load scenarios data
print("Loading enhanced_scenarios.json...")
scenarios_data = load_json_data('enhanced_scenarios.json')

print("DEBUG: Scenarios data keys:", list(scenarios_data.keys()) if scenarios_data else "No data")

if scenarios_data and 'enhanced_scenarios' in scenarios_data:
    print("DEBUG: Enhanced scenarios keys:", list(scenarios_data['enhanced_scenarios'].keys()))
    
    if 'dragon_hunters_path' in scenarios_data['enhanced_scenarios']:
        dragon_scenario = scenarios_data['enhanced_scenarios']['dragon_hunters_path']
        print("DEBUG: Dragon scenario keys:", list(dragon_scenario.keys()))
        
        story_nodes = dragon_scenario.get('story_nodes', {})
        print("DEBUG: story_nodes type:", type(story_nodes))
        print("DEBUG: story_nodes keys:", list(story_nodes.keys()) if isinstance(story_nodes, dict) else "Not a dict")
        
        if isinstance(story_nodes, dict) and 'start' in story_nodes:
            start_node = story_nodes['start']
            print("DEBUG: start node found!")
            print("DEBUG: start node keys:", list(start_node.keys()))
            print("DEBUG: start node choices count:", len(start_node.get('choices', [])))
        else:
            print("DEBUG: start node NOT found!")
            print("DEBUG: story_nodes content:", story_nodes)
    else:
        print("DEBUG: dragon_hunters_path not found in enhanced_scenarios")
else:
    print("DEBUG: enhanced_scenarios not found in scenarios_data")
