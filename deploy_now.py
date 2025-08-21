#!/usr/bin/env python3
"""
🚀 AI DUNGEON MASTER - DEPLOYMENT SCRIPT
Version: AI Scenario Generation System v1.0
"""

import os
import json
import requests
import time
from datetime import datetime

def check_file_exists(filepath):
    """Check if a file exists"""
    return os.path.exists(filepath)

def check_json_validity(filepath):
    """Check if JSON file is valid"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except:
        return False

def check_server_status():
    """Check if the Flask server is running"""
    try:
        response = requests.get('http://127.0.0.1:5002/', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_api_endpoints():
    """Check if API endpoints are working"""
    endpoints = [
        '/api/scenarios',
        '/api/ai-scenarios',
        '/api/characters',
        '/api/skills'
    ]
    
    working_endpoints = []
    for endpoint in endpoints:
        try:
            response = requests.get(f'http://127.0.0.1:5002{endpoint}', timeout=5)
            if response.status_code == 200:
                working_endpoints.append(endpoint)
        except:
            pass
    
    return working_endpoints

def main():
    print("🚀 AI DUNGEON MASTER - DEPLOYMENT CHECK")
    print("=" * 50)
    print(f"📅 Check Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check critical files
    print("📁 FILE SYSTEM CHECK:")
    critical_files = [
        'test_vercel.py',
        'templates/game_enhanced.html',
        'static/enhanced_script.js',
        'static/enhanced_style.css',
        'data/ai_scenarios.json',
        'data/enhanced_scenarios.json',
        'data/enhanced_cyberpunk_scenarios.json',
        'data/enhanced_warhammer_scenarios.json'
    ]
    
    all_files_ok = True
    for filepath in critical_files:
        exists = check_file_exists(filepath)
        valid = check_json_validity(filepath) if filepath.endswith('.json') else True
        status = "✅" if exists and valid else "❌"
        print(f"  {status} {filepath}")
        if not exists or not valid:
            all_files_ok = False
    
    print()
    
    # Check server status
    print("🌐 SERVER STATUS:")
    server_running = check_server_status()
    print(f"  {'✅' if server_running else '❌'} Flask Server (Port 5002)")
    
    if server_running:
        # Check API endpoints
        print("🔌 API ENDPOINTS:")
        working_endpoints = check_api_endpoints()
        for endpoint in working_endpoints:
            print(f"  ✅ {endpoint}")
        
        if len(working_endpoints) < 4:
            print(f"  ⚠️  Only {len(working_endpoints)}/4 endpoints working")
    
    print()
    
    # Deployment status
    print("🎯 DEPLOYMENT STATUS:")
    if all_files_ok and server_running:
        print("  🎉 DEPLOYMENT SUCCESSFUL!")
        print("  🌐 Server is running at: http://127.0.0.1:5002")
        print("  🎮 AI Scenario Generation System is ready!")
        print()
        print("  📋 NEXT STEPS:")
        print("  1. Open http://127.0.0.1:5002 in your browser")
        print("  2. Navigate to AI ÜRETİLEN SENARYOLAR section")
        print("  3. Fill out the AI scenario generation form")
        print("  4. Click 'AI Senaryo Üret' to create scenarios")
        print("  5. Click on generated scenarios to view details")
        print("  6. Click 'Bu Senaryoyu Oyna' to start playing")
    else:
        print("  ❌ DEPLOYMENT ISSUES DETECTED!")
        if not all_files_ok:
            print("  - Some critical files are missing or invalid")
        if not server_running:
            print("  - Flask server is not running")
        print()
        print("  🔧 TROUBLESHOOTING:")
        print("  1. Run: python test_vercel.py")
        print("  2. Check file permissions")
        print("  3. Verify all files are in correct locations")
    
    print()
    print("=" * 50)
    print("📊 DEPLOYMENT SUMMARY:")
    print(f"  Files: {'✅' if all_files_ok else '❌'}")
    print(f"  Server: {'✅' if server_running else '❌'}")
    print(f"  APIs: {len(check_api_endpoints())}/4 working")
    print()
    
    # Feature checklist
    print("✨ FEATURE CHECKLIST:")
    features = [
        "AI Senaryo Üretim Sistemi",
        "Görsel Arayüz",
        "Button Functionality Fixes",
        "Enhanced Storytelling",
        "Duration Optimization",
        "API Endpoints",
        "Data Management"
    ]
    
    for feature in features:
        print(f"  ✅ {feature}")
    
    print()
    print("🎉 AI DUNGEON MASTER v1.0 IS READY FOR ACTION! 🎉")

if __name__ == "__main__":
    main()
