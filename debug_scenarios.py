#!/usr/bin/env python3
"""
Debug script to see what scenarios endpoint returns
"""

import requests
import json

def debug_scenarios():
    """Debug what scenarios endpoint returns"""
    base_url = "https://ai-dungeon-master-main.vercel.app"
    
    print("🔍 Debugging scenarios endpoint...")
    
    try:
        response = requests.get(f"{base_url}/api/scenarios")
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
        print(f"Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("\n📄 Response structure:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:1000] + "...")
                
                # Check all top-level keys
                print(f"\n🔑 Top-level keys: {list(data.keys())}")
                
                # If there are scenarios, show the first few
                if 'scenarios' in data:
                    scenarios = data['scenarios']
                    print(f"\n📋 Found {len(scenarios)} scenarios in 'scenarios' key")
                    for i, scenario in enumerate(scenarios[:3]):  # Show first 3
                        print(f"  {i+1}. {scenario.get('title', 'No title')} (ID: {scenario.get('id', 'No ID')})")
                        
                if 'enhanced_scenarios' in data:
                    enhanced = data['enhanced_scenarios']
                    print(f"\n📋 Found {len(enhanced)} scenarios in 'enhanced_scenarios' key")
                    for scenario_id, scenario_data in list(enhanced.items())[:3]:  # Show first 3
                        print(f"  {scenario_id}: {scenario_data.get('title', 'No title')}")
                        
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"Raw response: {response.text[:500]}...")
        else:
            print(f"❌ Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_scenarios()
