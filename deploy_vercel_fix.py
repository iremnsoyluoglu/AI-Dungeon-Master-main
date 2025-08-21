#!/usr/bin/env python3
"""
Vercel Deployment Fix Script
This script fixes the Vercel deployment issues by ensuring proper build configuration.
"""

import os
import json
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
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_file_exists(filepath):
    """Check if a file exists"""
    return os.path.exists(filepath)

def create_build_script():
    """Create a build script for Vercel"""
    build_script = """#!/bin/bash
echo "🔨 Building React app..."
npm install
npm run build
echo "✅ Build completed"
"""
    
    with open("build.sh", "w") as f:
        f.write(build_script)
    
    # Make it executable
    os.chmod("build.sh", 0o755)
    print("✅ Created build.sh script")

def main():
    print("🚀 Starting Vercel Deployment Fix...")
    
    # Check if we're in the right directory
    if not check_file_exists("package.json"):
        print("❌ package.json not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check if React app exists
    if not check_file_exists("src/App.js"):
        print("❌ React app not found. Please ensure src/App.js exists.")
        sys.exit(1)
    
    # Install dependencies
    if run_command("npm install", "Installing dependencies") is None:
        sys.exit(1)
    
    # Create build script
    create_build_script()
    
    # Test build locally
    print("🧪 Testing build locally...")
    if run_command("npm run build", "Building React app") is None:
        print("❌ Build failed. Please check the errors above.")
        sys.exit(1)
    
    # Check if build directory was created
    if not check_file_exists("build"):
        print("❌ Build directory not created. Build may have failed.")
        sys.exit(1)
    
    print("✅ Local build successful!")
    
    # Create a simple index.html in public if it doesn't exist
    if not check_file_exists("public/index.html"):
        print("📝 Creating public/index.html...")
        html_content = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="AI Dungeon Master - Interactive RPG Game" />
    <title>AI Dungeon Master</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>"""
        
        with open("public/index.html", "w") as f:
            f.write(html_content)
        print("✅ Created public/index.html")
    
    print("\n🎉 Vercel deployment fix completed!")
    print("📋 Next steps:")
    print("1. Commit your changes: git add . && git commit -m 'Fix Vercel deployment'")
    print("2. Push to GitHub: git push origin main")
    print("3. Vercel will automatically redeploy")
    print("4. Check your deployment at: https://ai-dungeon-master-main.vercel.app/")

if __name__ == "__main__":
    main()
