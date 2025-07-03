#!/bin/bash

# AI Dungeon Master Setup Script
echo "🧙‍♂️ Setting up AI Dungeon Master..."

# Check if Python 3.8+ is installed
echo "📋 Checking Python version..."
python3 --version || {
    echo "❌ Python 3 is required. Please install Python 3.8 or higher."
    exit 1
}

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv ai_dm_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ai_dm_env/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating project structure..."
mkdir -p {src,data,config,logs,templates,static/{css,js,images},tests}

# Create subdirectories for organized code
mkdir -p src/{core,ai,game,utils,web}
mkdir -p data/{characters,campaigns,rules,worlds}
mkdir -p templates/{game,admin}

# Set up configuration files
echo "⚙️ Setting up configuration..."
cp config/config.example.yml config/config.yml 2>/dev/null || echo "Config example not found, will create default"

# Set permissions
chmod +x src/main.py 2>/dev/null || echo "Main script not found yet"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔐 Creating .env file..."
    cat > .env << 'EOF'
# AI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///ai_dm.db

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True

# Game Configuration
DEFAULT_SYSTEM=dnd5e
MAX_PLAYERS=6
SESSION_TIMEOUT=3600
EOF
fi

echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Add your API keys to the .env file"
echo "2. Run: source ai_dm_env/bin/activate"
echo "3. Run: python src/main.py"
echo ""
echo "📖 Check README.md for detailed instructions"