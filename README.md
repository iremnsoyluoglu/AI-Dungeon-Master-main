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

### Windows Kullanıcıları İçin (En Kolay Yöntem)

1. **Batch Dosyası ile Başlatma:**

   ```bash
   # Sadece çift tıklayın:
   start_app.bat
   ```

2. **PowerShell ile Başlatma:**
   ```powershell
   # PowerShell'de çalıştırın:
   .\start_app.ps1
   ```

### Manuel Başlatma

1. **Clone and Setup**:

   ```bash
   git clone <your-repo-url>
   cd AI-Dungeon-Master
   ```

2. **Configure API Keys**:
   Edit the `.env` file and add your API keys:

   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

3. **Run the Application**:

   ```bash
   python src/main.py
   ```

4. **Access the Web Interface**:
   Open your browser to `http://localhost:5050`

### Test Script'i ile Başlatma

```bash
# Otomatik test ve başlatma:
python test_app.py
```

## 🧪 Test Dosyaları

Proje içinde 3 farklı başlatma yöntemi bulunmaktadır:

1. **`test_app.py`** - Python test script'i

   - API endpoint'lerini test eder
   - Sunucuyu otomatik başlatır
   - Tarayıcıyı açar

2. **`start_app.bat`** - Windows batch dosyası

   - Çift tıklayarak başlatın
   - Otomatik tarayıcı açar

3. **`start_app.ps1`** - PowerShell script'i
   - PowerShell'de çalıştırın
   - Renkli çıktı ve detaylı bilgi

## 📁 Project Structure

```
AI-Dungeon-Master/
├── src/
│   ├── core/           # Core game engine
│   ├── ai/             # AI integration modules
│   ├── web/            # Web interface
│   └── main.py         # Application entry point
├── data/
│   ├── characters/     # Character data
│   ├── campaigns/      # Campaign saves
│   └── saves/          # Game saves
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── config/             # Configuration files
├── logs/               # Application logs
├── test_app.py         # Test script
├── start_app.bat       # Windows launcher
├── start_app.ps1       # PowerShell launcher
└── README.md           # This file
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
# Otomatik test:
python test_app.py

# Manuel test:
curl http://localhost:5050/api/health
curl http://localhost:5050/api/campaigns
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

### Available Endpoints:

- `GET /api/health` - System health check
- `GET /api/campaigns` - List available campaigns
- `GET /api/campaign/<id>` - Get campaign details
- `POST /api/game/session/start` - Start new game session
- `POST /api/game/roll-dice` - Roll dice
- `POST /api/ai/generate` - Generate AI content

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

## 🆘 Troubleshooting

### Common Issues:

1. **Port 5050 already in use:**

   ```bash
   # Windows:
   netstat -ano | findstr :5050
   taskkill /PID <PID> /F

   # Linux/Mac:
   lsof -i :5050
   kill -9 <PID>
   ```

2. **Python not found:**

   - Install Python 3.8+ from python.org
   - Add Python to PATH

3. **API key not working:**

   - Check .env file exists
   - Verify OPENAI_API_KEY is set correctly
   - Restart the application

4. **Butonlar çalışmıyor:**
   - Browser console'u açın (F12)
   - JavaScript hatalarını kontrol edin
   - Sayfayı yenileyin (Ctrl+F5)
