#!/usr/bin/env python3
"""
Simple Flask App for Testing
============================
A basic Flask application to test backend functionality
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Load data files
def load_json_file(filename):
    try:
        with open(f'data/{filename}', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Load data
character_classes = load_json_file('character_classes.json')
character_races = load_json_file('character_races.json')
scenarios = load_json_file('scenarios.json')

@app.route('/')
def index():
    return jsonify({
        'message': 'AI Dungeon Master Backend is running!',
        'status': 'healthy',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'services': {
            'character_classes': len(character_classes),
            'character_races': len(character_races),
            'scenarios': len(scenarios)
        }
    })

@app.route('/api/characters/classes')
def get_character_classes():
    return jsonify(character_classes)

@app.route('/api/characters/races')
def get_character_races():
    return jsonify(character_races)

@app.route('/api/scenarios')
def get_scenarios():
    # Convert scenarios to list format for frontend
    scenario_list = []
    for scenario_id, scenario_data in scenarios.items():
        scenario_list.append({
            'id': scenario_id,
            'title': scenario_data.get('title', 'Unknown'),
            'theme': scenario_data.get('theme', 'fantasy'),
            'difficulty': scenario_data.get('difficulty', 'medium'),
            'description': scenario_data.get('description', ''),
            'isFavorite': False,
            'createdAt': scenario_data.get('created_at', ''),
            'tags': [scenario_data.get('theme', 'fantasy')]
        })
    return jsonify(scenario_list)

@app.route('/api/characters', methods=['POST'])
def create_character():
    data = request.get_json()
    character_name = data.get('name', 'Unknown')
    character_class = data.get('characterClass', 'warrior')
    character_race = data.get('characterRace', 'human')
    
    # Create character data
    character = {
        'id': f'char_{len(character_classes) + 1}',
        'name': character_name,
        'class': character_class,
        'race': character_race,
        'level': 1,
        'xp': 0,
        'hp': 100,
        'attack': 10,
        'defense': 10
    }
    
    return jsonify({
        'success': True,
        'character': character,
        'message': f'Character {character_name} created successfully!'
    })

@app.route('/api/characters/<character_id>/level')
def get_character_level(character_id):
    # Mock character level data
    return jsonify({
        'level': 1,
        'xp': 0,
        'xp_to_next': 100,
        'skill_points': 2
    })

@app.route('/api/characters/<character_id>/skills')
def get_character_skills(character_id):
    # Mock skills data
    return jsonify({
        'class': 'warrior',
        'level': 1,
        'available_skills': [
            {
                'name': 'Shield Wall',
                'level_required': 2,
                'description': 'Kalkanla savunma yaparak düşman saldırısını engeller'
            }
        ],
        'unlocked_skills': []
    })

@app.route('/api/characters/<character_id>/gain_xp', methods=['POST'])
def gain_character_xp(character_id):
    data = request.get_json()
    xp_gained = data.get('xp', 0)
    
    return jsonify({
        'success': True,
        'xp_gained': xp_gained,
        'new_total_xp': xp_gained,
        'level_up': False,
        'message': f'Gained {xp_gained} XP!'
    })

@app.route('/api/characters/<character_id>/unlock_skill', methods=['POST'])
def unlock_character_skill(character_id):
    data = request.get_json()
    skill_name = data.get('skill_name', '')
    
    return jsonify({
        'success': True,
        'skill_unlocked': skill_name,
        'message': f'Skill {skill_name} unlocked successfully!'
    })

@app.route('/api/dice/roll', methods=['POST'])
def roll_dice():
    data = request.get_json()
    dice_type = data.get('type', 'd20')
    target = data.get('target', 10)
    
    import random
    if dice_type == 'd20':
        roll = random.randint(1, 20)
    elif dice_type == 'd6':
        roll = random.randint(1, 6)
    else:
        roll = random.randint(1, 20)
    
    success = roll >= target
    
    return jsonify({
        'roll': roll,
        'target': target,
        'success': success,
        'dice_type': dice_type,
        'message': f'Rolled {roll} on {dice_type} (target: {target})'
    })

if __name__ == '__main__':
    print("🚀 Starting AI Dungeon Master Backend...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/api/health")
    print("🎭 Character classes: http://localhost:5000/api/characters/classes")
    print("📚 Scenarios: http://localhost:5000/api/scenarios")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 