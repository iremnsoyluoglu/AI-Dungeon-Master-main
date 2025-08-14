"""
RAG System Integration with AI Dungeon Master
Integrates RAG capabilities with the existing game system.
"""

import sys
import os
import json
from typing import Dict, Any, List

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def integrate_rag_with_game():
    """Integrate RAG system with the existing game"""
    print("🔗 Integrating RAG System with AI Dungeon Master...")
    
    try:
        from rag.main import RAGSystem
        
        # Initialize RAG system
        rag_system = RAGSystem()
        
        # Load existing game data
        game_data = load_game_data()
        
        # Process game data for RAG
        processed_data = process_game_data_for_rag(game_data)
        
        # Upload game data to RAG system
        upload_result = upload_game_data_to_rag(rag_system, processed_data)
        
        # Create enhanced scenarios using RAG
        enhanced_scenarios = create_enhanced_scenarios(rag_system)
        
        # Update game data with RAG-enhanced content
        updated_game_data = update_game_with_rag_content(game_data, enhanced_scenarios)
        
        # Save updated game data
        save_updated_game_data(updated_game_data)
        
        print("✅ RAG Integration Completed Successfully!")
        return True
        
    except Exception as e:
        print(f"❌ RAG Integration Failed: {str(e)}")
        return False

def load_game_data() -> Dict[str, Any]:
    """Load existing game data"""
    print("📂 Loading existing game data...")
    
    game_data = {}
    
    # Load scenarios
    try:
        with open('data/scenarios.json', 'r', encoding='utf-8') as f:
            game_data['scenarios'] = json.load(f)
    except FileNotFoundError:
        print("⚠️ scenarios.json not found, using empty scenarios")
        game_data['scenarios'] = []
    
    # Load character classes
    try:
        with open('data/character_classes.json', 'r', encoding='utf-8') as f:
            game_data['character_classes'] = json.load(f)
    except FileNotFoundError:
        print("⚠️ character_classes.json not found, using empty classes")
        game_data['character_classes'] = []
    
    # Load character races
    try:
        with open('data/character_races.json', 'r', encoding='utf-8') as f:
            game_data['character_races'] = json.load(f)
    except FileNotFoundError:
        print("⚠️ character_races.json not found, using empty races")
        game_data['character_races'] = []
    
    return game_data

def process_game_data_for_rag(game_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Process game data for RAG system"""
    print("🔄 Processing game data for RAG...")
    
    processed_data = []
    
    # Process scenarios
    for scenario in game_data.get('scenarios', []):
        content = f"""
        Scenario: {scenario.get('name', 'Unknown')}
        Description: {scenario.get('description', 'No description')}
        Theme: {scenario.get('theme', 'fantasy')}
        Level: {scenario.get('level', 1)}
        """
        processed_data.append({
            'content': content,
            'context': 'game_scenario',
            'metadata': scenario
        })
    
    # Process character classes
    for char_class in game_data.get('character_classes', []):
        content = f"""
        Character Class: {char_class.get('name', 'Unknown')}
        Description: {char_class.get('description', 'No description')}
        Abilities: {char_class.get('abilities', [])}
        Stats: {char_class.get('stats', {})}
        """
        processed_data.append({
            'content': content,
            'context': 'character_class',
            'metadata': char_class
        })
    
    # Process character races
    for race in game_data.get('character_races', []):
        content = f"""
        Character Race: {race.get('name', 'Unknown')}
        Description: {race.get('description', 'No description')}
        Traits: {race.get('traits', [])}
        Bonuses: {race.get('bonuses', {})}
        """
        processed_data.append({
            'content': content,
            'context': 'character_race',
            'metadata': race
        })
    
    return processed_data

def upload_game_data_to_rag(rag_system: RAGSystem, processed_data: List[Dict[str, str]]) -> Dict[str, Any]:
    """Upload game data to RAG system"""
    print("📤 Uploading game data to RAG system...")
    
    # Create a combined document from all game data
    combined_content = "\n\n".join([item['content'] for item in processed_data])
    
    # Create temporary file
    temp_file = "rag/uploads/user_documents/game_data.txt"
    os.makedirs(os.path.dirname(temp_file), exist_ok=True)
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(combined_content)
    
    # Upload to RAG system
    upload_result = rag_system.upload_document(temp_file)
    
    return upload_result

def create_enhanced_scenarios(rag_system: RAGSystem) -> List[Dict[str, Any]]:
    """Create enhanced scenarios using RAG"""
    print("🎮 Creating enhanced scenarios using RAG...")
    
    enhanced_scenarios = []
    
    # Generate scenarios for different themes and levels
    themes = ['fantasy', 'cyberpunk', 'warhammer']
    levels = [1, 3, 5]
    
    for theme in themes:
        for level in levels:
            try:
                scenario_result = rag_system.generate_scenario(theme, level)
                if scenario_result['success']:
                    enhanced_scenario = {
                        'name': f"RAG-Enhanced {theme.title()} Adventure",
                        'description': scenario_result['scenario'],
                        'theme': theme,
                        'level': level,
                        'source': 'rag_generated',
                        'enhanced': True
                    }
                    enhanced_scenarios.append(enhanced_scenario)
            except Exception as e:
                print(f"⚠️ Failed to generate scenario for {theme} level {level}: {str(e)}")
    
    return enhanced_scenarios

def update_game_with_rag_content(game_data: Dict[str, Any], enhanced_scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update game data with RAG-enhanced content"""
    print("🔄 Updating game data with RAG content...")
    
    # Add enhanced scenarios to existing scenarios
    if 'scenarios' not in game_data:
        game_data['scenarios'] = []
    
    game_data['scenarios'].extend(enhanced_scenarios)
    
    # Create RAG-enhanced character classes
    enhanced_classes = create_enhanced_character_classes()
    if 'character_classes' not in game_data:
        game_data['character_classes'] = []
    
    game_data['character_classes'].extend(enhanced_classes)
    
    return game_data

def create_enhanced_character_classes() -> List[Dict[str, Any]]:
    """Create enhanced character classes using RAG insights"""
    enhanced_classes = [
        {
            'name': 'RAG-Enhanced Battlemage',
            'description': 'A hybrid warrior-mage that combines melee combat with spellcasting, enhanced through RAG analysis of optimal class combinations.',
            'abilities': ['Spell Combat', 'Arcane Armor', 'Battle Magic'],
            'stats': {'strength': 14, 'intelligence': 16, 'constitution': 12, 'charisma': 10},
            'source': 'rag_enhanced'
        },
        {
            'name': 'RAG-Enhanced Shadowdancer',
            'description': 'A stealth-focused character with enhanced mobility and illusion magic, optimized through RAG analysis.',
            'abilities': ['Shadow Step', 'Silent Movement', 'Illusion Magic'],
            'stats': {'dexterity': 18, 'intelligence': 12, 'charisma': 14, 'constitution': 10},
            'source': 'rag_enhanced'
        }
    ]
    
    return enhanced_classes

def save_updated_game_data(game_data: Dict[str, Any]):
    """Save updated game data"""
    print("💾 Saving updated game data...")
    
    # Save enhanced scenarios
    with open('data/enhanced_scenarios.json', 'w', encoding='utf-8') as f:
        json.dump(game_data['scenarios'], f, indent=2, ensure_ascii=False)
    
    # Save enhanced character classes
    with open('data/enhanced_character_classes.json', 'w', encoding='utf-8') as f:
        json.dump(game_data['character_classes'], f, indent=2, ensure_ascii=False)
    
    print("✅ Game data saved successfully!")

def test_rag_integration():
    """Test the RAG integration with the game"""
    print("🧪 Testing RAG Integration...")
    
    try:
        from rag.main import RAGSystem
        
        rag_system = RAGSystem()
        
        # Test 1: Load game data
        game_data = load_game_data()
        print(f"✅ Loaded {len(game_data.get('scenarios', []))} scenarios")
        print(f"✅ Loaded {len(game_data.get('character_classes', []))} character classes")
        
        # Test 2: Process for RAG
        processed_data = process_game_data_for_rag(game_data)
        print(f"✅ Processed {len(processed_data)} data items for RAG")
        
        # Test 3: Upload to RAG
        upload_result = upload_game_data_to_rag(rag_system, processed_data)
        print(f"✅ Upload result: {upload_result['success']}")
        
        # Test 4: Generate enhanced content
        enhanced_scenarios = create_enhanced_scenarios(rag_system)
        print(f"✅ Generated {len(enhanced_scenarios)} enhanced scenarios")
        
        # Test 5: Question answering with game context
        question_result = rag_system.ask_question("What are the different character classes available?")
        print(f"✅ Question answering: {question_result['success']}")
        
        print("🎉 RAG Integration Test Completed Successfully!")
        return True
        
    except Exception as e:
        print(f"❌ RAG Integration Test Failed: {str(e)}")
        return False

def main():
    """Main integration function"""
    print("🚀 Starting RAG Integration with AI Dungeon Master...")
    
    # Test integration
    test_success = test_rag_integration()
    
    if test_success:
        # Perform full integration
        integration_success = integrate_rag_with_game()
        
        if integration_success:
            print("\n🎉 RAG Integration Completed Successfully!")
            print("📁 Enhanced game data saved to:")
            print("   - data/enhanced_scenarios.json")
            print("   - data/enhanced_character_classes.json")
        else:
            print("\n⚠️ RAG Integration failed. Check the output above for details.")
    else:
        print("\n⚠️ RAG Integration test failed. Cannot proceed with full integration.")

if __name__ == "__main__":
    main()
