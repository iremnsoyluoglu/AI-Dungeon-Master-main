#!/usr/bin/env python3
"""
Check AI Dungeon Master Deployment Status
========================================
This script checks the current deployment status and verifies functionality
"""

import requests
import json
import sys
from datetime import datetime

def check_url(url, description):
    """Check if a URL is accessible"""
    try:
        print(f"🔍 Checking {description}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {description} is working (Status: {response.status_code})")
            return True
        else:
            print(f"⚠️  {description} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_api_endpoint(url, endpoint, description):
    """Check a specific API endpoint"""
    try:
        print(f"🔍 Checking {description}...")
        response = requests.get(f"{url}{endpoint}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {description} is working")
            if 'features' in data:
                print(f"   📋 Features: {len(data['features'])} available")
            return True
        else:
            print(f"⚠️  {description} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {description} failed: {e}")
        return False
    except json.JSONDecodeError:
        print(f"⚠️  {description} returned invalid JSON")
        return False

def main():
    print("🔍 AI Dungeon Master Deployment Status Check")
    print("=" * 50)
    print(f"📅 Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Base URL
    base_url = "https://ai-dungeon-master-main.vercel.app"
    
    print(f"\n🌐 Base URL: {base_url}")
    
    # Check main page
    main_working = check_url(base_url, "Main page")
    
    # Check login page
    login_working = check_url(f"{base_url}/login", "Login page")
    
    # Check game page
    game_working = check_url(f"{base_url}/game", "Game page")
    
    # Check health API
    health_working = check_api_endpoint(base_url, "/api/health", "Health API")
    
    # Check scenarios API
    scenarios_working = check_api_endpoint(base_url, "/api/scenarios", "Scenarios API")
    
    # Check characters API
    characters_working = check_api_endpoint(base_url, "/api/characters", "Characters API")
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    total_checks = 6
    working_checks = sum([main_working, login_working, game_working, 
                         health_working, scenarios_working, characters_working])
    
    print(f"✅ Working: {working_checks}/{total_checks}")
    print(f"❌ Failed: {total_checks - working_checks}/{total_checks}")
    
    if working_checks == total_checks:
        print("\n🎉 All systems are working correctly!")
        print("Your AI Dungeon Master application is fully functional.")
    elif working_checks >= 4:
        print("\n⚠️  Most systems are working, but some issues detected.")
        print("The application should be mostly functional.")
    else:
        print("\n❌ Multiple systems are not working.")
        print("The application needs attention.")
    
    print(f"\n🔗 Visit your application: {base_url}")

if __name__ == "__main__":
    main()
