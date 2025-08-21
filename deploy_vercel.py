#!/usr/bin/env python3
"""
Vercel Deployment Script
=======================
This script helps deploy the AI Dungeon Master to Vercel
"""

import os
import subprocess
import sys

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚀 AI Dungeon Master - Vercel Deployment")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("vercel.json"):
        print("❌ Error: vercel.json not found. Please run this script from the project root.")
        return
    
    # Check if test_vercel.py exists
    if not os.path.exists("test_vercel.py"):
        print("❌ Error: test_vercel.py not found.")
        return
    
    print("✅ Configuration files found")
    
    # Check if Vercel CLI is installed
    print("\n📋 Checking Vercel CLI...")
    success, stdout, stderr = run_command("vercel --version")
    
    if not success:
        print("❌ Vercel CLI not found. Please install it first:")
        print("   npm install -g vercel")
        print("   or visit: https://vercel.com/docs/cli")
        return
    
    print(f"✅ Vercel CLI found: {stdout.strip()}")
    
    # Deploy to Vercel
    print("\n🚀 Deploying to Vercel...")
    success, stdout, stderr = run_command("vercel --prod")
    
    if success:
        print("✅ Deployment successful!")
        print("\n📋 Deployment output:")
        print(stdout)
        
        # Try to extract the URL
        lines = stdout.split('\n')
        for line in lines:
            if 'https://' in line and 'vercel.app' in line:
                print(f"\n🌐 Your app is live at: {line.strip()}")
                break
    else:
        print("❌ Deployment failed!")
        print("Error output:")
        print(stderr)
        print("\n📋 Full output:")
        print(stdout)

if __name__ == "__main__":
    main()
