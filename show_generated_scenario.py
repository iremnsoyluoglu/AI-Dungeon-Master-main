#!/usr/bin/env python3
"""
Display generated scenario details
"""

import json
import os

def show_generated_scenario():
    """Show the generated scenario from file upload"""
    
    print("🎮 GENERATED SCENARIO DETAILS")
    print("=" * 60)
    
    # Load the generated scenario
    scenario_file = 'data/ai_scenarios.json'
    
    if not os.path.exists(scenario_file):
        print("❌ No generated scenarios found. Please upload a file first.")
        return
    
    try:
        with open(scenario_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        scenarios = data.get('scenarios', [])
        if not scenarios:
            print("❌ No scenarios found in the file.")
            return
        
        # Get the latest scenario
        scenario = scenarios[-1]
        
        print(f"📋 TITLE: {scenario.get('title', 'Unknown')}")
        print(f"🎭 THEME: {scenario.get('theme', 'Unknown')}")
        print(f"⚡ DIFFICULTY: {scenario.get('difficulty', 'Unknown')}")
        print(f"📊 WORD COUNT: {scenario.get('word_count', 'Unknown')}")
        print(f"⏱️ DURATION: {scenario.get('duration', 'Unknown')} minutes")
        print(f"📈 LEVEL RANGE: {scenario.get('min_level', 'Unknown')}-{scenario.get('max_level', 'Unknown')}")
        print(f"📁 SOURCE FILE: {scenario.get('file_source', 'Unknown')}")
        print()
        
        print("📖 DESCRIPTION:")
        print(scenario.get('description', 'No description available'))
        print()
        
        # Show story nodes in detail
        story_nodes = scenario.get('story_nodes', {})
        print(f"🎯 STORY NODES ({len(story_nodes)} total):")
        print("-" * 40)
        
        for node_id, node in story_nodes.items():
            print(f"\n📍 NODE: {node_id}")
            print(f"   📝 Title: {node.get('title', 'No title')}")
            print(f"   📖 Description: {node.get('description', 'No description')[:100]}...")
            
            choices = node.get('choices', [])
            print(f"   🎯 Choices ({len(choices)}):")
            for i, choice in enumerate(choices, 1):
                print(f"      {i}. {choice.get('text', 'No text')}")
                print(f"         → Next: {choice.get('next_node', 'None')}")
                print(f"         → Effect: {choice.get('effect', 'None')}")
        
        print()
        
        # Show NPCs
        npcs = scenario.get('npc_relationships', {})
        if npcs:
            print(f"👥 NPCs ({len(npcs)} total):")
            print("-" * 20)
            for npc_id, npc in npcs.items():
                print(f"   • {npc.get('name', 'Unknown')}")
                print(f"     Trust Level: {npc.get('trust_level', 0)}")
                print(f"     Status: {npc.get('relationship_status', 'Unknown')}")
                print(f"     Impact: {npc.get('ending_impact', 'Unknown')}")
        
        print()
        
        # Show quest chains
        quests = scenario.get('quest_chains', {})
        if quests:
            print(f"🎯 QUEST CHAINS ({len(quests)} total):")
            print("-" * 30)
            for quest_id, quest in quests.items():
                print(f"   • {quest.get('title', 'Unknown Quest')}")
                print(f"     Prerequisites: {quest.get('prerequisites', [])}")
                print(f"     Quests: {quest.get('quests', [])}")
                print(f"     Rewards: {quest.get('rewards', {})}")
        
        print()
        
        # Show levels
        levels = scenario.get('levels', {})
        if levels:
            print(f"📊 LEVELS ({len(levels)} total):")
            print("-" * 20)
            for level_id, level in levels.items():
                print(f"   • {level.get('title', 'Unknown Level')}")
                print(f"     Description: {level.get('description', 'No description')}")
                print(f"     Level Range: {level.get('min_level', 'Unknown')}-{level.get('max_level', 'Unknown')}")
                print(f"     Enemies: {level.get('enemies', [])}")
                print(f"     Boss: {level.get('boss', 'None')}")
                print(f"     Side Quests: {level.get('side_quests', [])}")
        
        print()
        print("✅ Scenario analysis completed!")
        print("🎮 This scenario is ready to be played!")
        
    except Exception as e:
        print(f"❌ Error reading scenario: {e}")

if __name__ == "__main__":
    show_generated_scenario()
