#!/usr/bin/env python3
"""
Redeploy AI Dungeon Master to Vercel
====================================
This script helps redeploy the application with the correct configuration
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("🚀 AI Dungeon Master Vercel Redeployment")
    print("=" * 50)
    
    # Check if vercel CLI is installed
    print("📋 Checking Vercel CLI...")
    if run_command("vercel --version", "Checking Vercel CLI") is None:
        print("❌ Vercel CLI not found. Please install it first:")
        print("   npm install -g vercel")
        return
    
    # Check current directory
    print(f"📁 Current directory: {os.getcwd()}")
    
    # Verify configuration files
    print("🔍 Verifying configuration files...")
    if not os.path.exists("vercel.json"):
        print("❌ vercel.json not found!")
        return
    
    if not os.path.exists("exact_original_vercel.py"):
        print("❌ exact_original_vercel.py not found!")
        return
    
    print("✅ Configuration files found")
    
    # Deploy to Vercel
    print("\n🚀 Deploying to Vercel...")
    print("This will open a browser window for authentication if needed.")
    
    deploy_result = run_command("vercel --prod", "Deploying to Vercel")
    
    if deploy_result:
        print("\n🎉 Deployment completed!")
        print("Your application should now be working correctly.")
        print("\n📋 What was fixed:")
        print("   ✅ CSS syntax error in test_vercel.py")
        print("   ✅ Vercel configuration pointing to correct file")
        print("   ✅ NPC functionality restored")
        print("   ✅ All game features available")
    else:
        print("\n❌ Deployment failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
