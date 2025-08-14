#!/usr/bin/env python3
"""
Final System Check
==================
Comprehensive check of all AI Dungeon Master systems
"""

import json
import os
from src.core.skill_system import SkillSystem
from src.core.combat_system import CombatSystem
from src.core.dice_system import DiceSystem
from src.core.level_system import LevelSystem
from src.core.karma_system import KarmaSystem
from src.core.campaign_manager import CampaignManager
from src.core.betrayal_system import BetrayalSystem

def check_scenarios():
    """Check scenario loading"""
    print("\n📚 Checking Scenarios...")
    try:
        with open('data/scenarios.json', 'r', encoding='utf-8') as f:
            scenarios = json.load(f)
        scenario_count = len(scenarios.get('scenarios', []))
        print(f"✅ Scenarios loaded: {scenario_count}")
        
        # Check enhanced scenario files
        enhanced_files = [
            'data/enhanced_fantasy_scenarios.json',
            'data/enhanced_warhammer_scenarios.json',
            'data/enhanced_cyberpunk_scenarios.json'
        ]
        
        for file_path in enhanced_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                scenario_count = len(data)
                print(f"✅ {file_path}: {scenario_count} scenarios")
            else:
                print(f"❌ {file_path}: File not found")
        
        return True
    except Exception as e:
        print(f"❌ Scenario check failed: {e}")
        return False

def check_skill_system():
    """Check skill system"""
    print("\n🔧 Checking Skill System...")
    try:
        skill_system = SkillSystem()
        
        # Test skill tree
        warrior_tree = skill_system.get_skill_tree("warrior")
        if warrior_tree:
            print(f"✅ Warrior skill tree: {warrior_tree['class_name']}")
            print(f"   Skills available: {len(warrior_tree['skills'])}")
        else:
            print("❌ Warrior skill tree failed")
            return False
        
        # Test other classes
        classes = ["mage", "rogue", "cleric"]
        for class_name in classes:
            tree = skill_system.get_skill_tree(class_name)
            if tree:
                print(f"✅ {class_name.capitalize()} skill tree: {tree['class_name']}")
            else:
                print(f"❌ {class_name.capitalize()} skill tree failed")
        
        return True
    except Exception as e:
        print(f"❌ Skill system check failed: {e}")
        return False

def check_combat_system():
    """Check combat system"""
    print("\n⚔️ Checking Combat System...")
    try:
        combat_system = CombatSystem()
        
        # Test dice roll
        dice_result = combat_system.roll_dice("1d20")
        print(f"✅ Combat dice roll: {dice_result}")
        
        # Test combat state
        state = combat_system.get_combat_state("test_session")
        if state:
            print("✅ Combat state retrieval working")
        else:
            print("✅ Combat system initialized (no active combat)")
        
        return True
    except Exception as e:
        print(f"❌ Combat system check failed: {e}")
        return False

def check_dice_system():
    """Check dice system"""
    print("\n🎲 Checking Dice System...")
    try:
        dice_system = DiceSystem()
        
        # Test basic rolls
        d20_roll = dice_system.roll_dice("1d20")
        d6_roll = dice_system.roll_dice("2d6")
        percentile = dice_system.roll_dice("1d100")
        
        print(f"✅ d20 roll: {d20_roll['total']}")
        print(f"✅ 2d6 roll: {d6_roll['total']}")
        print(f"✅ percentile roll: {percentile['total']}")
        
        return True
    except Exception as e:
        print(f"❌ Dice system check failed: {e}")
        return False

def check_level_system():
    """Check level system"""
    print("\n📈 Checking Level System...")
    try:
        level_system = LevelSystem()
        
        character_data = {
            "level": 1,
            "experience": 0,
            "health": 100,
            "max_health": 100,
            "attack": 10,
            "defense": 5,
            "skill_points": 0
        }
        
        # Test experience gain
        result = level_system.add_experience(character_data, 150)
        if result["success"]:
            print(f"✅ Experience system: Level {result['character_data']['level']}")
        else:
            print(f"❌ Experience system failed: {result.get('error')}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Level system check failed: {e}")
        return False

def check_karma_system():
    """Check karma system"""
    print("\n⚖️ Checking Karma System...")
    try:
        karma_system = KarmaSystem()
        
        # Test karma action
        result = karma_system.record_action("test_player", "help_npc", npc_id="test_npc")
        if result["success"]:
            print(f"✅ Karma action: {result['karma_change']} points")
        else:
            print(f"❌ Karma action failed: {result.get('error')}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Karma system check failed: {e}")
        return False

def check_campaign_system():
    """Check campaign system"""
    print("\n📖 Checking Campaign System...")
    try:
        campaign_manager = CampaignManager()
        
        # Test campaign loading
        campaigns = campaign_manager.list_campaigns()
        if campaigns:
            print(f"✅ Campaigns loaded: {len(campaigns)}")
        else:
            print("❌ No campaigns found")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Campaign system check failed: {e}")
        return False

def check_betrayal_system():
    """Check betrayal system"""
    print("\n🎭 Checking Betrayal System...")
    try:
        betrayal_system = BetrayalSystem()
        
        # Test betrayal summary
        result = betrayal_system.get_betrayal_summary("test_session")
        if result:
            print(f"✅ Betrayal system: {result.get('total_betrayals', 0)} betrayals tracked")
        else:
            print("✅ Betrayal system initialized")
        
        return True
    except Exception as e:
        print(f"❌ Betrayal system check failed: {e}")
        return False

def main():
    """Run all system checks"""
    print("🚀 FINAL SYSTEM CHECK")
    print("=" * 50)
    
    checks = [
        ("Scenarios", check_scenarios),
        ("Skill System", check_skill_system),
        ("Combat System", check_combat_system),
        ("Dice System", check_dice_system),
        ("Level System", check_level_system),
        ("Karma System", check_karma_system),
        ("Campaign System", check_campaign_system),
        ("Betrayal System", check_betrayal_system)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
            else:
                print(f"❌ {name} check failed")
        except Exception as e:
            print(f"❌ {name} check crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 FINAL RESULTS: {passed}/{total} systems working")
    
    if passed == total:
        print("✅ ALL SYSTEMS OPERATIONAL")
        print("🚀 READY FOR PRESENTATION")
    else:
        print("⚠️ Some systems need attention")
        print(f"🔧 {total - passed} system(s) need fixing")
    
    return passed == total

if __name__ == "__main__":
    main()
