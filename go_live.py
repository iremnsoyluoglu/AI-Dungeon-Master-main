#!/usr/bin/env python3
"""
AI Dungeon Master - LIVE DEMO SCRIPT

This script starts the game in LIVE mode for public access.
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def start_flask_server():
    """Start Flask server in production mode."""
    print("Starting Flask server in LIVE mode...")
    os.environ['FLASK_ENV'] = 'production'
    subprocess.run([sys.executable, 'app.py'])

def start_streamlit_server():
    """Start Streamlit server for demo."""
    print("Starting Streamlit demo...")
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py', '--server.port', '8501'])

def open_browser():
    """Open browser to the live game."""
    time.sleep(3)  # Wait for servers to start
    print("Opening browser to LIVE game...")
    webbrowser.open('http://localhost:5002/enhanced')
    webbrowser.open('http://localhost:8501')

def main():
    """Main function to start everything."""
    print("AI DUNGEON MASTER - GOING LIVE!")
    print("=" * 50)
    print("Starting servers...")
    print("Flask Server: http://localhost:5002")
    print("Streamlit Demo: http://localhost:8501")
    print("=" * 50)
    
    # Start Flask server in background
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start Streamlit server in background
    streamlit_thread = threading.Thread(target=start_streamlit_server)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        print("AI Dungeon Master is now OFFLINE")

if __name__ == "__main__":
    main()
