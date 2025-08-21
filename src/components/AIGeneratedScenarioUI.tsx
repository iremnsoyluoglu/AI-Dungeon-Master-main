import React, { useState, useRef } from 'react';
import './AIGeneratedScenarioUI.css';

interface AIGeneratedScenario {
  id: string;
  title: string;
  description: string;
  theme: string;
  difficulty: string;
  genre: string;
  complexity: string;
  estimatedPlayTime: number;
  story_nodes: {
    [key: string]: {
      id: string;
      title: string;
      description: string;
      choices: Array<{
        id: string;
        text: string;
        next_node: string;
        effect: any;
      }>;
    };
  };
  npc_relationships: {
    [key: string]: {
      name: string;
      trust_level: number;
      quests_completed: number;
      relationship_status: string;
      ending_impact: string;
    };
  };
  quest_chains: {
    [key: string]: {
      title: string;
      prerequisites: string[];
      quests: string[];
      rewards: any;
    };
  };
  ending_variations: {
    [key: string]: {
      requirements: any;
      description: string;
    };
  };
  combat_scenes: Array<{
    id: string;
    title: string;
    enemies: string[];
    boss?: string;
    rounds: number;
    status_effects: string[];
  }>;
  decision_points: Array<{
    id: string;
    title: string;
    description: string;
    choices: string[];
    consequences: string[];
  }>;
}

interface AIGeneratedScenarioUIProps {
  onScenarioGenerated: (scenario: AIGeneratedScenario) => void;
  onThemeAdded: (theme: string) => void;
  onBack?: () => void;
}

export const AIGeneratedScenarioUI: React.FC<AIGeneratedScenarioUIProps> = ({
  onScenarioGenerated,
  onThemeAdded,
  onBack
}) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [selectedTheme, setSelectedTheme] = useState('custom');
  const [selectedDifficulty, setSelectedDifficulty] = useState('medium');
  const [selectedGenre, setSelectedGenre] = useState('fantasy');
  const [customPrompt, setCustomPrompt] = useState('');
  const [generatedScenario, setGeneratedScenario] = useState<AIGeneratedScenario | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const themes = [
    { id: 'custom', name: '🎨 Özel Tema', description: 'Kendi temanızı belirleyin' },
    { id: 'epic_fantasy', name: '🐉 Epik Fantazi', description: 'Ejderhalar, büyücüler ve destansı maceralar' },
    { id: 'cyberpunk_revolution', name: '🌃 Cyberpunk Devrimi', description: 'AI\'lar, mega şirketler ve dijital savaş' },
    { id: 'space_war', name: '🚀 Uzay Savaşı', description: 'Galaksiler arası çatışma ve uzay gemileri' },
    { id: 'horror_mystery', name: '👻 Korku Gizemi', description: 'Karanlık sırlar ve korkunç gerçekler' },
    { id: 'post_apocalyptic', name: '☢️ Post-Apokaliptik', description: 'Nükleer savaş sonrası dünya' },
    { id: 'steampunk_adventure', name: '⚙️ Steampunk Macera', description: 'Buhar gücü ve mekanik harikalar' },
    { id: 'superhero_origin', name: '🦸 Süper Kahraman Kökeni', description: 'Güçlerin keşfi ve kahramanlık yolu' }
  ];

  const difficulties = [
    { id: 'easy', name: 'Kolay', description: 'Yeni başlayanlar için' },
    { id: 'medium', name: 'Orta', description: 'Deneyimli oyuncular için' },
    { id: 'hard', name: 'Zor', description: 'Uzman oyuncular için' },
    { id: 'very_hard', name: 'Çok Zor', description: 'Master seviye' }
  ];

  const genres = [
    { id: 'fantasy', name: 'Fantazi', description: 'Büyü ve macera' },
    { id: 'sci_fi', name: 'Bilim Kurgu', description: 'Teknoloji ve uzay' },
    { id: 'horror', name: 'Korku', description: 'Korku ve gerilim' },
    { id: 'mystery', name: 'Gizem', description: 'Gizem ve dedektiflik' },
    { id: 'action', name: 'Aksiyon', description: 'Savaş ve macera' },
    { id: 'drama', name: 'Drama', description: 'Duygusal hikayeler' }
  ];

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      setError(null);
    }
  };

  const handleGenerateScenario = async () => {
    if (!uploadedFile && !customPrompt) {
      setError('Lütfen bir dosya yükleyin veya özel bir prompt yazın');
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      const formData = new FormData();
      if (uploadedFile) {
        formData.append('file', uploadedFile);
      }
      formData.append('theme', selectedTheme);
      formData.append('difficulty', selectedDifficulty);
      formData.append('genre', selectedGenre);
      formData.append('customPrompt', customPrompt);

      const response = await fetch('/api/ai/scenarios/generate', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Senaryo üretme başarısız');
      }

      const scenario: AIGeneratedScenario = await response.json();
      
      // Sidebar'a "AI ile Üretilen" temasını ekle
      onThemeAdded('ai_generated');
      
      // Üretilen senaryoyu kaydet ve göster
      setGeneratedScenario(scenario);
      onScenarioGenerated(scenario);
      
      console.log('AI Generated Scenario:', scenario);
    } catch (error) {
      console.error('Scenario generation error:', error);
      setError(`Senaryo üretme hatası: ${error}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSaveScenario = async () => {
    if (!generatedScenario) return;

    try {
      const response = await fetch('/api/scenarios/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...generatedScenario,
          source: 'ai_generated',
          generated_at: new Date().toISOString()
        })
      });

      if (response.ok) {
        alert('Senaryo başarıyla kaydedildi!');
      } else {
        throw new Error('Kaydetme başarısız');
      }
    } catch (error) {
      console.error('Save error:', error);
      setError(`Kaydetme hatası: ${error}`);
    }
  };

  return (
    <div className="ai-generated-scenario-ui">
      <div className="ai-header">
        <div className="header-left">
          {onBack && (
            <button className="back-button" onClick={onBack}>
              ← Geri
            </button>
          )}
        </div>
        <div className="header-center">
          <h2>🤖 AI ile Senaryo Üret</h2>
          <p>Dosya yükleyin veya özel prompt yazın, AI karmaşık senaryolar üretsin!</p>
        </div>
      </div>

      <div className="ai-controls">
        {/* File Upload Section */}
        <div className="upload-section">
          <h3>📁 Dosya Yükle</h3>
          <div className="file-upload-area">
            <input
              ref={fileInputRef}
              type="file"
              accept=".txt,.md,.json,.pdf"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
            <button 
              className="upload-button"
              onClick={() => fileInputRef.current?.click()}
            >
              {uploadedFile ? `📄 ${uploadedFile.name}` : '📁 Dosya Seç'}
            </button>
            {uploadedFile && (
              <button 
                className="clear-button"
                onClick={() => setUploadedFile(null)}
              >
                ❌ Temizle
              </button>
            )}
          </div>
        </div>

        {/* Custom Prompt Section */}
        <div className="prompt-section">
          <h3>✍️ Özel Prompt</h3>
          <textarea
            value={customPrompt}
            onChange={(e) => setCustomPrompt(e.target.value)}
            placeholder="Senaryonuzun detaylarını yazın... Örnek: 'Karanlık bir ormanda kaybolmuş bir grup maceracı, eski bir tapınağı keşfediyor...'"
            rows={4}
            className="custom-prompt-input"
          />
        </div>

        {/* Configuration Section */}
        <div className="config-section">
          <h3>⚙️ Senaryo Ayarları</h3>
          
          <div className="config-grid">
            <div className="config-item">
              <label>Tema:</label>
              <select 
                value={selectedTheme} 
                onChange={(e) => setSelectedTheme(e.target.value)}
                className="config-select"
              >
                {themes.map(theme => (
                  <option key={theme.id} value={theme.id}>
                    {theme.name}
                  </option>
                ))}
              </select>
              <small>{themes.find(t => t.id === selectedTheme)?.description}</small>
            </div>

            <div className="config-item">
              <label>Zorluk:</label>
              <select 
                value={selectedDifficulty} 
                onChange={(e) => setSelectedDifficulty(e.target.value)}
                className="config-select"
              >
                {difficulties.map(diff => (
                  <option key={diff.id} value={diff.id}>
                    {diff.name}
                  </option>
                ))}
              </select>
              <small>{difficulties.find(d => d.id === selectedDifficulty)?.description}</small>
            </div>

            <div className="config-item">
              <label>Tür:</label>
              <select 
                value={selectedGenre} 
                onChange={(e) => setSelectedGenre(e.target.value)}
                className="config-select"
              >
                {genres.map(genre => (
                  <option key={genre.id} value={genre.id}>
                    {genre.name}
                  </option>
                ))}
              </select>
              <small>{genres.find(g => g.id === selectedGenre)?.description}</small>
            </div>
          </div>
        </div>

        {/* Generate Button */}
        <div className="generate-section">
          <button 
            className="generate-button"
            onClick={handleGenerateScenario}
            disabled={isGenerating || (!uploadedFile && !customPrompt)}
          >
            {isGenerating ? '🤖 Üretiliyor...' : '🚀 Senaryo Üret'}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="error-message">
            ❌ {error}
          </div>
        )}
      </div>

      {/* Generated Scenario Display */}
      {generatedScenario && (
        <div className="generated-scenario">
          <div className="scenario-header">
            <h3>🎯 Üretilen Senaryo: {generatedScenario.title}</h3>
            <button className="save-button" onClick={handleSaveScenario}>
              💾 Kaydet
            </button>
          </div>

          <div className="scenario-details">
            <div className="scenario-info">
              <p><strong>Açıklama:</strong> {generatedScenario.description}</p>
              <p><strong>Tema:</strong> {generatedScenario.theme}</p>
              <p><strong>Zorluk:</strong> {generatedScenario.difficulty}</p>
              <p><strong>Tahmini Süre:</strong> {generatedScenario.estimatedPlayTime} dakika</p>
            </div>

            <div className="scenario-stats">
              <div className="stat-item">
                <span className="stat-number">{Object.keys(generatedScenario.story_nodes).length}</span>
                <span className="stat-label">Karar Noktası</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{generatedScenario.combat_scenes.length}</span>
                <span className="stat-label">Savaş Sahnesi</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{Object.keys(generatedScenario.ending_variations).length}</span>
                <span className="stat-label">Farklı Son</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{Object.keys(generatedScenario.npc_relationships).length}</span>
                <span className="stat-label">NPC</span>
              </div>
            </div>

            <div className="scenario-preview">
              <h4>📖 Senaryo Önizlemesi</h4>
              <div className="preview-content">
                {Object.entries(generatedScenario.story_nodes).slice(0, 3).map(([nodeId, node]) => (
                  <div key={nodeId} className="preview-node">
                    <h5>{node.title}</h5>
                    <p>{node.description.substring(0, 150)}...</p>
                    <div className="preview-choices">
                      {node.choices.slice(0, 2).map((choice, index) => (
                        <span key={index} className="choice-preview">
                          {choice.text.substring(0, 50)}...
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
