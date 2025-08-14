# AI Dungeon Master - Gelişmiş Hikaye Anlatım Oyunu

## 🎮 Proje Hakkında

AI Dungeon Master, yapay zeka destekli gelişmiş bir hikaye anlatım oyunudur. Oyuncular farklı temalarda (Fantasy, Warhammer 40K, Cyberpunk) karakterler oluşturur ve dinamik hikayeler yaşar. Oyun, contextual events, betrayal system, plot twists ve multiple endings gibi gelişmiş özellikler içerir.

## ✨ Özellikler

### 🤖 AI Agent Sistemi (Phase 4 - IMPLEMENTED ✅)
- **LangChain Agent Architecture**: 4 özelleştirilmiş AI agent'ı
- **Story Generation Agent**: Dinamik hikaye üretimi ve senaryo oluşturma
- **Character Management Agent**: Karakter oluşturma ve geliştirme
- **Game State Agent**: Oyun durumu yönetimi ve session tracking
- **Content Curator Agent**: İçerik kalite kontrolü ve doğrulama
- **Agent Orchestrator**: Tüm agent'ları koordine eden merkezi sistem
- **Automation System**: Günlük otomatik içerik üretimi
- **Memory Management**: ConversationBufferMemory ile context yönetimi

### 🔍 RAG & Fine-tuning Sistemi (Phase 5 - IMPLEMENTED ✅)
- **Retrieval-Augmented Generation**: Doküman tabanlı akıllı yanıt sistemi
- **ChromaDB Vector Database**: Gelişmiş vektör depolama ve arama
- **OpenAI Embeddings**: Doküman vektörizasyonu ve semantic search
- **Document Processing**: PDF ve TXT dosya işleme ve chunking
- **Fine-tuning Pipeline**: Özel veri setleri ile model eğitimi
- **HuggingFace Transformers**: Custom model training ve optimizasyon
- **RAG Pipeline**: Soru-cevap ve senaryo üretimi için entegre sistem
- **Training Data Preparation**: Otomatik eğitim verisi hazırlama

### 🎭 Gelişmiş Hikaye Sistemi
- **Contextual Events**: Hikaye bağlamına göre özel olaylar
- **Betrayal System**: NPC'lerin ihanet etme şansı
- **Plot Twists**: Beklenmedik hikaye gelişmeleri
- **Multiple Endings**: Farklı sonlar ve yollar

### 🎨 Görsel Tasarım
- **3-Panel Layout**: Sol, orta, sağ panel düzeni
- **Glass Morphism**: Modern cam efekti tasarım
- **Atmospheric Background**: Atmosferik arka plan
- **Colored Glowing Borders**: Renkli parlayan kenarlıklar
- **Responsive Design**: Mobil uyumlu tasarım

### 🎯 Oyun Mekanikleri
- **Dice Roll System**: Zar atma mekanizması
- **Character Progression**: Karakter gelişimi
- **Karma System**: Ahlaki seçim sistemi
- **Relationship Tracking**: NPC ilişki takibi
- **Emotional Arcs**: Duygusal gelişim takibi

### 🌟 Tema Sistemi
- **Fantasy**: Ejderhalar, büyü, orman maceraları
- **Warhammer 40K**: Uzay savaşları, Space Marines
- **Cyberpunk**: Siberpunk dünyası, AI, şehir maceraları

## 🚀 Kurulum

### Gereksinimler
- Python 3.12.3+
- Flask 3.1.3+
- LangChain 0.1.0+
- ChromaDB 0.4.18+
- Transformers 4.35.0+
- Modern web browser

### Adım Adım Kurulum

1. **Repository'yi klonlayın**
```bash
git clone https://github.com/yourusername/ai-dungeon-master.git
cd ai-dungeon-master
```

2. **Python dependencies'leri yükleyin**
```bash
pip install -r requirements.txt
```

3. **AI Agent sistemini test edin**
```bash
python test_agents.py
```

4. **RAG sistemini test edin**
```bash
python test_rag_system.py
```

5. **Uygulamayı başlatın**
```bash
python app.py
```

6. **Tarayıcıda açın**
```
http://localhost:5002
```

## 🎮 Nasıl Oynanır

### 1. Tema Seçimi
- Sol panelden bir tema seçin (Fantasy, Warhammer 40K, Cyberpunk)
- Her tema farklı ırk ve sınıf seçenekleri sunar

### 2. Karakter Oluşturma
- Irk seçin (Human, Elf, Dwarf, Space Marine, vb.)
- Sınıf seçin (Warrior, Mage, Rogue, vb.)
- Karakter istatistikleri otomatik hesaplanır

### 3. Senaryo Seçimi
- Orta panelden bir senaryo seçin
- Senaryo açıklamasını okuyun
- "Senaryo Başlat" butonuna tıklayın

### 4. Oyun Deneyimi
- Hikaye metnini okuyun
- Seçeneklerden birini seçin
- Dice roll'ları bekleyin
- Sonuçları görün

### 5. Gelişmiş Özellikler
- **Betrayal Alerts**: Kırmızı uyarılar
- **Plot Twist Notifications**: Sarı bildirimler
- **Event Log**: Sağ panelde olay geçmişi
- **Character Stats**: Sol panelde karakter bilgileri

## 📁 Proje Yapısı

```
AI-Dungeon-Master/
├── app.py                          # Ana Flask uygulaması
├── requirements.txt                 # Python dependencies
├── README.md                       # Bu dosya
├── user-flow.md                    # Kullanıcı akışı
├── tech-stack.md                   # Teknoloji stack'i
├── agents/                         # AI Agent Sistemi (Phase 4)
│   ├── __init__.py                # Agent package initialization
│   ├── agent_orchestrator.py      # Merkezi agent koordinatörü
│   ├── story_generation_agent.py  # Hikaye üretim agent'ı
│   ├── character_management_agent.py # Karakter yönetim agent'ı
│   ├── game_state_agent.py        # Oyun durumu agent'ı
│   └── content_curator_agent.py   # İçerik küratör agent'ı
├── rag/                           # RAG & Fine-tuning Sistemi (Phase 5)
│   ├── __init__.py                # RAG package initialization
│   ├── main.py                    # Ana RAG sistemi
│   ├── document_processor.py      # Doküman işleme
│   ├── vector_store.py           # Vektör depolama yönetimi
│   ├── rag_pipeline.py           # RAG pipeline
│   ├── fine_tuning/              # Fine-tuning modülleri
│   │   ├── __init__.py
│   │   ├── data_preparation.py   # Eğitim verisi hazırlama
│   │   └── fine_tuning_pipeline.py # Model eğitimi
│   ├── config/                   # Konfigürasyon dosyaları
│   │   ├── rag_config.json
│   │   └── fine_tuning_config.json
│   ├── uploads/                  # Kullanıcı dokümanları
│   ├── vector_db/                # Vektör veritabanı
│   └── fine_tuned_model/         # Eğitilmiş modeller
├── data/                          # Oyun verileri
│   ├── enhanced_scenarios.json    # Gelişmiş senaryolar
│   ├── character_classes.json     # Sınıf bilgileri
│   ├── character_races.json       # Irk bilgileri
│   ├── betrayals.json            # İhanet sistemi
│   └── plot_twists.json          # Plot twist verileri
├── static/                        # Statik dosyalar
│   ├── mystical_style.css        # Ana CSS dosyası
│   └── script.js                 # JavaScript kodu
├── templates/                     # HTML template'leri
│   └── game_mystical.html        # Ana oyun sayfası
├── src/                          # Kaynak kodlar
│   ├── ai/                       # AI modülleri
│   ├── core/                     # Çekirdek sistemler
│   └── scenarios/                # Senaryo yönetimi
├── test_agents.py                # Agent sistemi testleri
├── test_rag_system.py            # RAG sistemi testleri
├── integrate_rag_with_game.py    # RAG-game entegrasyonu
└── automation_runner.py          # Otomatik görev çalıştırıcı
```

## 🎯 Özellik Detayları

### AI Agent Sistemi (Phase 4)
- **Story Generation Agent**: Dinamik hikaye üretimi, senaryo oluşturma, plot twist generation
- **Character Management Agent**: Karakter oluşturma, stat yönetimi, progression tracking
- **Game State Agent**: Session yönetimi, save/load operations, state persistence
- **Content Curator Agent**: İçerik kalite kontrolü, validation, content enhancement
- **Agent Orchestrator**: Tüm agent'ları koordine eden merkezi sistem
- **Automation**: Günlük otomatik içerik üretimi ve curation

### RAG & Fine-tuning Sistemi (Phase 5)
- **Document Processing**: PDF ve TXT dosya yükleme, chunking, metadata management
- **Vector Storage**: ChromaDB ile vektör depolama ve similarity search
- **RAG Pipeline**: Soru-cevap sistemi, senaryo üretimi, content generation
- **Fine-tuning**: Custom veri setleri ile model eğitimi ve optimizasyon
- **Training Data**: Otomatik eğitim verisi hazırlama ve validation
- **Model Management**: Eğitilmiş modellerin yüklenmesi ve kullanımı

### Contextual Events
- Hikaye bağlamına göre özel olaylar tetiklenir
- Forest location, combat situation, NPC interaction gibi
- Her context için farklı betrayal ve plot twist şansları

### Betrayal System
- NPC'ler oyuncuyu kandırabilir
- Trust building emotional arc'i etkiler
- Betrayal sayısı takip edilir

### Plot Twist Engine
- Beklenmedik hikaye gelişmeleri
- Power progression emotional arc'i etkiler
- Plot twist sayısı takip edilir

### Dice Roll System
- Skill-based checks (Perception, Investigation, vb.)
- Success/failure consequences
- Hidden consequences ve bonuslar

### Multiple Endings
- Her senaryo için 3-5 farklı son
- Heroic, Power, Balanced, Light, Shadow endings
- Ending summary ile detaylı sonuç

## 🔧 Geliştirme

### AI Agent Sistemi Geliştirme
1. `agents/` klasöründeki agent'ları özelleştirin
2. `agent_orchestrator.py` ile yeni workflow'lar ekleyin
3. `test_agents.py` ile agent fonksiyonlarını test edin
4. `automation_runner.py` ile otomatik görevler ekleyin

### RAG Sistemi Geliştirme
1. `rag/` klasöründeki modülleri kullanın
2. `test_rag_system.py` ile RAG fonksiyonlarını test edin
3. `integrate_rag_with_game.py` ile oyun entegrasyonu yapın
4. Fine-tuning için custom veri setleri hazırlayın

### Yeni Senaryo Ekleme
1. `data/enhanced_scenarios.json` dosyasına yeni senaryo ekleyin
2. Story nodes, choices, contextual events tanımlayın
3. Betrayal ve plot twist şanslarını ayarlayın

### Yeni Tema Ekleme
1. `static/script.js` dosyasında `themeData` objesine ekleyin
2. Races, classes, scenarios tanımlayın
3. CSS'te yeni tema renkleri ekleyin

### AI Entegrasyonu
1. `src/ai/` klasöründeki modülleri kullanın
2. LLM API'lerini entegre edin
3. Prompt engineering ile hikaye üretimi

## 🐛 Sorun Giderme

### Yaygın Sorunlar

**Oyun yüklenmiyor**
- Flask server'ın çalıştığından emin olun
- Port 5002'nin açık olduğunu kontrol edin
- Browser cache'ini temizleyin

**AI Agent sistemi çalışmıyor**
- `pip install langchain-openai` komutunu çalıştırın
- OpenAI API key'inizi kontrol edin
- `test_agents.py` ile agent'ları test edin

**RAG sistemi çalışmıyor**
- `pip install chromadb datasets accelerate` komutunu çalıştırın
- `test_rag_system.py` ile RAG sistemini test edin
- Vector database dosyalarının varlığını kontrol edin

**CSS stilleri görünmüyor**
- `static/mystical_style.css` dosyasının varlığını kontrol edin
- Browser developer tools'da CSS hatalarını kontrol edin

**JavaScript hataları**
- Browser console'da hata mesajlarını kontrol edin
- `static/script.js` dosyasının yüklendiğinden emin olun

## 📊 Performans

### Optimizasyonlar
- Static file caching
- Image compression
- Code minification
- Lazy loading
- Vector database indexing
- Model caching

### Monitoring
- Flask logging
- Error tracking
- Performance monitoring
- User analytics
- Agent performance metrics
- RAG system analytics

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🙏 Teşekkürler

- Flask framework ekibine
- LangChain ve OpenAI ekibine
- ChromaDB ve Hugging Face ekibine
- Font Awesome ikonlarına
- Açık kaynak topluluğuna

## 📞 İletişim

- **GitHub**: [yourusername/ai-dungeon-master](https://github.com/yourusername/ai-dungeon-master)
- **Email**: your.email@example.com
- **Issues**: GitHub Issues sayfasını kullanın

---

**AI Dungeon Master** - Gelişmiş hikaye anlatım deneyimi için yapay zeka teknolojisini kullanarak oluşturulmuş interaktif bir oyun projesidir. 🎮✨

**Phase 4 (Agent Architecture) ve Phase 5 (RAG & Fine-tuning) başarıyla implement edilmiştir!** 🚀
