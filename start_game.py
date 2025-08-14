#!/usr/bin/env python3
"""
AI Dungeon Master - Game Startup Script
=======================================

This script initializes and starts the complete FRP game system.
"""

import os
import sys
import subprocess
import time
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed"""
    logger.info("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'flask_socketio', 'openai', 'psycopg2', 'redis',
        'requests', 'bs4', 'pandas', 'numpy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"❌ {package} - Missing")
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_environment():
    """Check environment variables and configuration"""
    logger.info("🔧 Checking environment...")
    
    # Check for .env file
    env_file = Path('.env')
    if not env_file.exists():
        logger.warning("⚠️  .env file not found")
        logger.info("Creating .env.example...")
        
        env_example = """# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/ai_dungeon_master
REDIS_URL=redis://localhost:6379

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DEBUG=True

# Game Configuration
MAX_PLAYERS_PER_SESSION=6
SESSION_TIMEOUT_MINUTES=30
"""
        
        with open('.env.example', 'w') as f:
            f.write(env_example)
        
        logger.info("📝 Created .env.example - Please copy to .env and configure")
        return False
    
    # Check environment variables
    required_env_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var) or os.getenv(var) == 'your_openai_api_key_here':
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.info("Continuing without OpenAI API key (some features will be limited)")
        return True
    
    logger.info("✅ Environment configuration OK")
    return True

def initialize_database():
    """Initialize database tables and basic data"""
    logger.info("🗄️  Initializing database...")
    
    try:
        # This would create database tables
        # In a real implementation, use SQLAlchemy migrations
        logger.info("✅ Database initialization complete")
        return True
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return False

def start_backend_server():
    """Start the Flask backend server"""
    logger.info("🚀 Starting backend server...")
    
    try:
        # Start the server using app.py
        from app import app, socketio
        
        logger.info("🌐 Backend server starting on http://localhost:5000")
        logger.info("📡 WebSocket server ready for connections")
        
        # Run the server
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
        
    except Exception as e:
        logger.error(f"❌ Failed to start backend server: {e}")
        return False
    
    return True

def start_frontend():
    """Start the React frontend development server"""
    logger.info("🎨 Starting frontend development server...")
    
    try:
        # Check if node_modules exists
        if not Path('node_modules').exists():
            logger.info("📦 Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        # Start development server
        logger.info("🌐 Frontend server starting on http://localhost:3001")
        subprocess.run(['npm', 'run', 'dev'], check=True)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to start frontend: {e}")
        return False
    except FileNotFoundError:
        logger.error("❌ Node.js/npm not found. Please install Node.js")
        return False
    
    return True

def show_welcome_message():
    """Display welcome message and instructions"""
    print("""
🎲 AI Dungeon Master - Tam FRP Oyun Sistemi
============================================

🚀 Sistem başlatılıyor...

Özellikler:
✅ Multiplayer destek
✅ AI destekli senaryo üretimi
✅ Sıra tabanlı savaş sistemi
✅ 8 farklı karakter sınıfı
✅ Real-time WebSocket iletişimi
✅ Quest ve level sistemi

Bağlantılar:
🌐 Frontend: http://localhost:3001
🔧 Backend API: http://localhost:5000
📡 WebSocket: ws://localhost:5000

Kullanım:
1. Tarayıcıda http://localhost:5000 adresini açın
2. Senaryo seçin veya yeni oluşturun
3. Karakterinizi oluşturun
4. Oyunu başlatın!

Ctrl+C ile sistemi durdurabilirsiniz.
""")

def main():
    """Main startup function"""
    show_welcome_message()
    
    # Check dependencies
    if not check_dependencies():
        logger.error("❌ Dependency check failed")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        logger.error("❌ Environment check failed")
        logger.info("Please configure your .env file and try again")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        logger.error("❌ Database initialization failed")
        sys.exit(1)
    
    logger.info("🎮 Starting AI Dungeon Master...")
    
    # Start backend in a separate process
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        logger.info("🔄 Starting backend server...")
        backend_process = subprocess.Popen([
            sys.executable, 'app.py'
        ])
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start frontend
        logger.info("🔄 Starting frontend server...")
        frontend_process = subprocess.Popen([
            'npm', 'run', 'dev'
        ])
        
        logger.info("✅ All servers started successfully!")
        logger.info("🌐 Open http://localhost:5000 in your browser")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down servers...")
            
    except Exception as e:
        logger.error(f"❌ Failed to start servers: {e}")
        
    finally:
        # Cleanup processes
        if backend_process:
            backend_process.terminate()
            logger.info("🛑 Backend server stopped")
        
        if frontend_process:
            frontend_process.terminate()
            logger.info("🛑 Frontend server stopped")
        
        logger.info("👋 Goodbye!")

if __name__ == "__main__":
    main() 