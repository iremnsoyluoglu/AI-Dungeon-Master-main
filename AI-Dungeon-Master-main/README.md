# 🧙‍♂️ AI Dungeon Master

An intelligent AI-powered Fantasy Role-Playing Game Master that creates immersive, dynamic adventures using advanced language models.

## ✨ Features

- **Intelligent Storytelling**: AI-powered narrative generation and world-building
- **Dynamic NPCs**: Character interactions with persistent memory and personality
- **Rule Management**: Support for multiple RPG systems (D&D 5e, Pathfinder, custom)
- **Campaign Management**: Persistent game state and character progression
- **Web Interface**: Modern, real-time web-based gaming interface
- **Voice Support**: Optional text-to-speech and speech recognition
- **Dice Rolling**: Integrated dice mechanics with custom rule sets
- **Character Sheets**: Digital character management and progression

## 🚀 Quick Start

1. **Clone and Setup**:
   ```bash
   git clone <your-repo-url>
   cd AI-Dungeon-Master
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Configure API Keys**:
   Edit the `.env` file and add your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

3. **Run the Application**:
   ```bash
   source ai_dm_env/bin/activate
   python src/main.py
   ```

4. **Access the Web Interface**:
   Open your browser to `http://localhost:5000`

## 📁 Project Structure

```
AI-Dungeon-Master/
├── src/
│   ├── core/           # Core game engine
│   ├── ai/             # AI integration modules
│   ├── game/           # Game logic and rules
│   ├── utils/          # Utility functions
│   ├── web/            # Web interface
│   └── main.py         # Application entry point
├── data/
│   ├── characters/     # Character data
│   ├── campaigns/      # Campaign saves
│   ├── rules/          # Rule systems
│   └── worlds/         # World templates
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── config/             # Configuration files
├── tests/              # Unit tests
└── logs/               # Application logs
```

## 🎯 Usage

### Starting a New Campaign
1. Create a new campaign through the web interface
2. Set the game system (D&D 5e, Pathfinder, etc.)
3. Define the world setting and initial scenario
4. Invite players to join

### Managing Characters
- Create and customize player characters
- Track stats, inventory, and progression
- Handle NPC interactions and relationships

### AI Game Master Features
- **Narrative Generation**: Create dynamic storylines
- **World Building**: Generate locations, NPCs, and quests
- **Combat Management**: Handle initiative, actions, and outcomes
- **Decision Making**: Respond to player actions intelligently

## ⚙️ Configuration

Edit `config/config.yml` to customize:
- AI model preferences
- Game system defaults
- Web server settings
- Database configuration

## 🧪 Development

### Running Tests
```bash
source ai_dm_env/bin/activate
pytest tests/
```

### Code Formatting
```bash
black src/
flake8 src/
```

## 📚 API Documentation

The project includes RESTful APIs for:
- Campaign management
- Character operations
- Game state handling
- AI interactions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude
- The D&D and RPG communities for inspiration
