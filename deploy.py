#!/usr/bin/env python3
"""
AI Dungeon Master - LIVE DEPLOYMENT SCRIPT

This script deploys the AI Dungeon Master game to multiple platforms:
- Local Flask Server
- Streamlit Cloud
- Heroku
- Railway
- Render
- Vercel (Frontend)
- GitHub Pages

MAKE THE GAME LIVE AND PUBLISHED!
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

class LiveDeployment:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.deployment_config = {
            "app_name": "ai-dungeon-master",
            "version": "1.0.0",
            "description": "AI-Powered Interactive Storytelling Game - LIFE ITSELF",
            "author": "AI Dungeon Master Team",
            "license": "MIT"
        }
    
    def create_deployment_files(self):
        """Create all necessary deployment files for LIVE publishing."""
        print("🚀 Creating LIVE deployment files...")
        
        # 1. Create Procfile for Heroku
        self.create_procfile()
        
        # 2. Create runtime.txt for Python version
        self.create_runtime_txt()
        
        # 3. Create app.json for Heroku
        self.create_app_json()
        
        # 4. Create vercel.json for Vercel
        self.create_vercel_json()
        
        # 5. Create railway.json for Railway
        self.create_railway_json()
        
        # 6. Create render.yaml for Render
        self.create_render_yaml()
        
        # 7. Create streamlit deployment config
        self.create_streamlit_config()
        
        # 8. Create Docker files
        self.create_docker_files()
        
        print("✅ All deployment files created!")
    
    def create_procfile(self):
        """Create Procfile for Heroku deployment."""
        procfile_content = """web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
worker: python automation_runner.py"""
        
        with open(self.project_root / "Procfile", "w") as f:
            f.write(procfile_content)
        print("✅ Procfile created for Heroku")
    
    def create_runtime_txt(self):
        """Create runtime.txt for Python version."""
        runtime_content = "python-3.11.7"
        
        with open(self.project_root / "runtime.txt", "w") as f:
            f.write(runtime_content)
        print("✅ runtime.txt created")
    
    def create_app_json(self):
        """Create app.json for Heroku deployment."""
        app_config = {
            "name": self.deployment_config["app_name"],
            "description": self.deployment_config["description"],
            "repository": "https://github.com/your-username/ai-dungeon-master",
            "logo": "https://raw.githubusercontent.com/your-username/ai-dungeon-master/main/static/images/logo.png",
            "keywords": ["ai", "gaming", "storytelling", "rpg", "interactive", "fantasy", "warhammer", "cyberpunk"],
            "env": {
                "OPENAI_API_KEY": {
                    "description": "OpenAI API Key for AI features",
                    "required": False
                },
                "FLASK_ENV": {
                    "description": "Flask environment",
                    "value": "production"
                }
            },
            "formation": {
                "web": {
                    "quantity": 1,
                    "size": "basic"
                }
            },
            "buildpacks": [
                {"url": "heroku/python"}
            ]
        }
        
        with open(self.project_root / "app.json", "w") as f:
            json.dump(app_config, f, indent=2)
        print("✅ app.json created for Heroku")
    
    def create_vercel_json(self):
        """Create vercel.json for Vercel deployment."""
        vercel_config = {
            "version": 2,
            "builds": [
                {
                    "src": "app.py",
                    "use": "@vercel/python"
                }
            ],
            "routes": [
                {
                    "src": "/(.*)",
                    "dest": "app.py"
                }
            ],
            "env": {
                "FLASK_ENV": "production"
            }
        }
        
        with open(self.project_root / "vercel.json", "w") as f:
            json.dump(vercel_config, f, indent=2)
        print("✅ vercel.json created")
    
    def create_railway_json(self):
        """Create railway.json for Railway deployment."""
        railway_config = {
            "$schema": "https://railway.app/railway.schema.json",
            "build": {
                "builder": "NIXPACKS"
            },
            "deploy": {
                "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --workers 4",
                "healthcheckPath": "/",
                "healthcheckTimeout": 100,
                "restartPolicyType": "ON_FAILURE",
                "restartPolicyMaxRetries": 10
            }
        }
        
        with open(self.project_root / "railway.json", "w") as f:
            json.dump(railway_config, f, indent=2)
        print("✅ railway.json created")
    
    def create_render_yaml(self):
        """Create render.yaml for Render deployment."""
        render_config = """services:
  - type: web
    name: ai-dungeon-master
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4
    envVars:
      - key: FLASK_ENV
        value: production
      - key: OPENAI_API_KEY
        sync: false
    healthCheckPath: /
    autoDeploy: true"""
        
        with open(self.project_root / "render.yaml", "w") as f:
            f.write(render_config)
        print("✅ render.yaml created")
    
    def create_streamlit_config(self):
        """Create Streamlit configuration for cloud deployment."""
        streamlit_config = """[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true"""
        
        with open(self.project_root / ".streamlit" / "config.toml", "w") as f:
            f.write(streamlit_config)
        print("✅ Streamlit config created")
    
    def create_docker_files(self):
        """Create Docker files for containerized deployment."""
        # Dockerfile
        dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5002

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5002", "--workers", "4", "--timeout", "120"]"""
        
        with open(self.project_root / "Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        # docker-compose.yml
        docker_compose_content = """version: '3.8'

services:
  ai-dungeon-master:
    build: .
    ports:
      - "5002:5002"
    environment:
      - FLASK_ENV=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    restart: unless-stopped"""
        
        with open(self.project_root / "docker-compose.yml", "w") as f:
            f.write(docker_compose_content)
        
        print("✅ Docker files created")
    
    def create_github_actions(self):
        """Create GitHub Actions for automated deployment."""
        workflows_dir = self.project_root / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # Deploy to multiple platforms
        deploy_workflow = """name: Deploy AI Dungeon Master

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest

  deploy-heroku:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.14
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
        heroku_email: ${{ secrets.HEROKU_EMAIL }}

  deploy-railway:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Railway
      uses: railway/deploy@v1.0.0
      with:
        railway_token: ${{ secrets.RAILWAY_TOKEN }}

  deploy-render:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Render
      run: |
        curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}"""
        
        with open(workflows_dir / "deploy.yml", "w") as f:
            f.write(deploy_workflow)
        
        print("✅ GitHub Actions workflow created")
    
    def create_live_demo_script(self):
        """Create a script to run the live demo."""
        demo_script = """#!/usr/bin/env python3
\"\"\"
AI Dungeon Master - LIVE DEMO SCRIPT

This script starts the game in LIVE mode for public access.
\"\"\"

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def start_flask_server():
    \"\"\"Start Flask server in production mode.\"\"\"
    print("🚀 Starting Flask server in LIVE mode...")
    os.environ['FLASK_ENV'] = 'production'
    subprocess.run([sys.executable, 'app.py'])

def start_streamlit_server():
    \"\"\"Start Streamlit server for demo.\"\"\"
    print("🎮 Starting Streamlit demo...")
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py', '--server.port', '8501'])

def open_browser():
    \"\"\"Open browser to the live game.\"\"\"
    time.sleep(3)  # Wait for servers to start
    print("🌐 Opening browser to LIVE game...")
    webbrowser.open('http://localhost:5002/enhanced')
    webbrowser.open('http://localhost:8501')

def main():
    \"\"\"Main function to start everything.\"\"\"
    print("🎮 AI DUNGEON MASTER - GOING LIVE!")
    print("=" * 50)
    print("🚀 Starting servers...")
    print("🌐 Flask Server: http://localhost:5002")
    print("🎮 Streamlit Demo: http://localhost:8501")
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
        print("\\n🛑 Shutting down servers...")
        print("✅ AI Dungeon Master is now OFFLINE")

if __name__ == "__main__":
    main()"""
        
        with open(self.project_root / "go_live.py", "w") as f:
            f.write(demo_script)
        
        # Make it executable
        os.chmod(self.project_root / "go_live.py", 0o755)
        print("✅ Live demo script created")
    
    def create_deployment_guide(self):
        """Create a comprehensive deployment guide."""
        guide_content = """# 🚀 AI DUNGEON MASTER - LIVE DEPLOYMENT GUIDE

## 🎮 MAKE THE GAME LIVE AND PUBLISHED!

This guide will help you deploy the AI Dungeon Master game to multiple platforms so it's LIVE and accessible to everyone!

### 🌐 Quick Start - Local Live Demo

```bash
# Start the game LIVE locally
python go_live.py
```

This will start both Flask and Streamlit servers and open your browser automatically!

### 🚀 Platform Deployments

#### 1. Heroku Deployment
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set OPENAI_API_KEY=your_api_key

# Deploy
git push heroku main
```

#### 2. Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy
railway up
```

#### 3. Render Deployment
```bash
# Connect your GitHub repo to Render
# Render will automatically deploy on push
```

#### 4. Vercel Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

#### 5. Streamlit Cloud
```bash
# Push to GitHub
# Connect to Streamlit Cloud
# Deploy automatically
```

### 🔧 Environment Variables

Set these environment variables for full functionality:

```bash
FLASK_ENV=production
OPENAI_API_KEY=your_openai_api_key
FLASK_SECRET_KEY=your_secret_key
```

### 📊 Monitoring & Analytics

The deployed app includes:
- Real-time game analytics
- Player feedback system
- Performance monitoring
- Error tracking

### 🌍 Public URLs

Once deployed, your game will be available at:
- **Heroku**: https://your-app-name.herokuapp.com
- **Railway**: https://your-app-name.railway.app
- **Render**: https://your-app-name.onrender.com
- **Vercel**: https://your-app-name.vercel.app
- **Streamlit Cloud**: https://your-app-name.streamlit.app

### 🎯 Features Available in LIVE Version

✅ **LIFE ITSELF Scenarios** - Immersive storytelling
✅ **AI-Powered Story Generation** - Dynamic narratives
✅ **Character System** - Full RPG mechanics
✅ **Combat System** - Skill-based battles
✅ **Quest System** - NPC interactions
✅ **Save/Load System** - Progress persistence
✅ **Multi-Theme Support** - Fantasy, Warhammer, Cyberpunk
✅ **Real-time Updates** - Live game state
✅ **Mobile Responsive** - Play anywhere
✅ **Social Features** - Share adventures

### 🚨 Troubleshooting

If deployment fails:
1. Check environment variables
2. Verify requirements.txt
3. Check logs for errors
4. Ensure all files are committed

### 📞 Support

For deployment issues:
- Check the logs
- Review environment setup
- Verify API keys
- Contact support team

---

## 🎮 YOUR GAME IS NOW LIVE AND PUBLISHED!

Players can now access your AI Dungeon Master game from anywhere in the world!
"""
        
        with open(self.project_root / "DEPLOYMENT_GUIDE.md", "w") as f:
            f.write(guide_content)
        print("✅ Deployment guide created")
    
    def deploy_all(self):
        """Deploy to all platforms."""
        print("🚀 AI DUNGEON MASTER - GOING LIVE ON ALL PLATFORMS!")
        print("=" * 60)
        
        # Create all deployment files
        self.create_deployment_files()
        self.create_github_actions()
        self.create_live_demo_script()
        self.create_deployment_guide()
        
        print("=" * 60)
        print("✅ ALL DEPLOYMENT FILES CREATED!")
        print("🎮 Your game is ready to go LIVE!")
        print("=" * 60)
        print("📋 Next steps:")
        print("1. Run: python go_live.py (for local demo)")
        print("2. Push to GitHub for cloud deployment")
        print("3. Follow DEPLOYMENT_GUIDE.md for platform setup")
        print("=" * 60)

def main():
    """Main deployment function."""
    deployer = LiveDeployment()
    deployer.deploy_all()

if __name__ == "__main__":
    main()
