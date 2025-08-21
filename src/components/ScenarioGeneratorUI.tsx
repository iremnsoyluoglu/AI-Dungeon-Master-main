import React, { useState } from "react";
import { LearnedScenarioGenerator } from "../services/LearnedScenarioGenerator";
import { RPGScenario, ScenarioKnowledge } from "../types/comic";
import "./ScenarioGeneratorUI.css";

interface ScenarioGeneratorUIProps {
  knowledgeBase: ScenarioKnowledge | null;
}

export const ScenarioGeneratorUI: React.FC<ScenarioGeneratorUIProps> = ({
  knowledgeBase,
}) => {
  const [generatedScenario, setGeneratedScenario] =
    useState<RPGScenario | null>(null);
  const [selectedTheme, setSelectedTheme] = useState<string>("dungeon");
  const [selectedDifficulty, setSelectedDifficulty] = useState<
    "easy" | "medium" | "hard"
  >("medium");
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // Dosya yükleme state'leri
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [fileContent, setFileContent] = useState<string>("");
  const [isReadingFile, setIsReadingFile] = useState<boolean>(false);
  const [fileError, setFileError] = useState<string | null>(null);

  // Dosya yükleme fonksiyonu
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Dosya tipini kontrol et
    const allowedTypes = [
      'text/plain',
      'text/markdown',
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];

    if (!allowedTypes.includes(file.type)) {
      setFileError("Sadece .txt, .md, .pdf, .doc, .docx dosyaları kabul edilir!");
      return;
    }

    setUploadedFile(file);
    setFileError(null);
    setFileContent("");
  };

  // Dosya okuma fonksiyonu
  const handleReadFile = async () => {
    if (!uploadedFile) {
      setFileError("Lütfen önce bir dosya yükleyin!");
      return;
    }

    setIsReadingFile(true);
    setFileError(null);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);

      const response = await fetch('/api/read-file', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Dosya okunamadı!');
      }

      const data = await response.json();
      setFileContent(data.content);
      
      // Dosya içeriğini senaryo üretimi için kullan
      console.log("Dosya içeriği okundu:", data.content);
      
    } catch (error) {
      console.error("Dosya okuma hatası:", error);
      setFileError(`Dosya okunamadı: ${error}`);
    } finally {
      setIsReadingFile(false);
    }
  };

  const handleGenerate = async () => {
    if (!knowledgeBase && !fileContent) {
      setError("Lütfen önce comic okuma işlemini tamamlayın veya bir dosya yükleyin!");
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      // API'ye senaryo üretimi için istek gönder
      const response = await fetch('/api/generate-scenario', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          theme: selectedTheme,
          difficulty: selectedDifficulty,
          fileContent: fileContent,
          knowledgeBase: knowledgeBase
        }),
      });

      if (!response.ok) {
        throw new Error('Senaryo üretilemedi!');
      }

      const data = await response.json();
      
      if (data.success) {
        setGeneratedScenario(data.scenario);
        console.log("Generated scenario:", data.scenario);
        
        // Başarı mesajı göster
        alert(data.message);
      } else {
        throw new Error(data.error || 'Senaryo üretilemedi!');
      }
      
    } catch (error) {
      console.error("Error generating scenario:", error);
      setError(`Failed to generate scenario: ${error}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleGenerateMultiple = async () => {
    if (!knowledgeBase && !fileContent) {
      setError("Lütfen önce comic okuma işlemini tamamlayın veya bir dosya yükleyin!");
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      // Birden fazla senaryo üret
      const scenarios = [];
      
      for (let i = 0; i < 3; i++) {
        const response = await fetch('/api/generate-scenario', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            theme: selectedTheme,
            difficulty: selectedDifficulty,
            fileContent: fileContent,
            knowledgeBase: knowledgeBase,
            scenarioNumber: i + 1
          }),
        });

        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            scenarios.push(data.scenario);
          }
        }
      }

      if (scenarios.length > 0) {
        setGeneratedScenario(scenarios[0]);
        console.log("Generated multiple scenarios:", scenarios);
        alert(`${scenarios.length} senaryo başarıyla üretildi!`);
      } else {
        throw new Error('Hiçbir senaryo üretilemedi!');
      }
      
    } catch (error) {
      console.error("Error generating scenarios:", error);
      setError(`Failed to generate scenarios: ${error}`);
    } finally {
      setIsGenerating(false);
    }
  };

  if (!knowledgeBase && !uploadedFile) {
    return (
      <div className="scenario-generator">
        <div className="no-knowledge">
          <h2>🎲 Scenario Generator</h2>
          <p>
            Please complete the comic reading process first or upload a file to generate RPG scenarios.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="scenario-generator">
      <div className="generator-header">
        <h2>🎲 Generate RPG Scenarios from Learned Patterns</h2>
        <p>Create unique adventures based on comic storytelling techniques or uploaded files</p>
      </div>

      {/* Dosya Yükleme Bölümü */}
      <div className="file-upload-section">
        <h3>📁 Dosya Yükle ve Oku</h3>
        <div className="file-upload-controls">
          <input
            type="file"
            accept=".txt,.md,.pdf,.doc,.docx"
            onChange={handleFileUpload}
            className="file-input"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="file-input-label">
            📁 Dosya Seç
          </label>
          
          {uploadedFile && (
            <div className="file-info">
              <span>📄 {uploadedFile.name}</span>
              <span>📊 {(uploadedFile.size / 1024).toFixed(1)} KB</span>
            </div>
          )}
          
          {uploadedFile && !fileContent && (
            <button
              onClick={handleReadFile}
              className="read-file-btn"
              disabled={isReadingFile}
            >
              {isReadingFile ? (
                <>
                  <span className="spinner"></span>
                  Dosya Okunuyor...
                </>
              ) : (
                "📖 Dosyayı Oku"
              )}
            </button>
          )}
          
          {fileError && (
            <div className="file-error">
              <span>⚠️ {fileError}</span>
              <button onClick={() => setFileError(null)}>×</button>
            </div>
          )}
          
          {fileContent && (
            <div className="file-content-preview">
              <h4>📄 Dosya İçeriği Önizleme:</h4>
              <div className="content-preview">
                {fileContent.substring(0, 300)}...
                {fileContent.length > 300 && (
                  <span className="content-length">
                    (Toplam {fileContent.length} karakter)
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="generator-controls">
        <div className="control-group">
          <label htmlFor="theme-select">Adventure Theme:</label>
          <select
            id="theme-select"
            value={selectedTheme}
            onChange={(e) => setSelectedTheme(e.target.value)}
            className="theme-select"
          >
            <option value="dungeon">Dungeon Crawl</option>
            <option value="mystery">Mystery Investigation</option>
            <option value="horror">Horror Survival</option>
            <option value="political">Political Intrigue</option>
            <option value="exploration">Wilderness Exploration</option>
            <option value="heist">Heist Mission</option>
            <option value="rescue">Rescue Mission</option>
            <option value="ritual">Ancient Ritual</option>
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="difficulty-select">Difficulty Level:</label>
          <select
            id="difficulty-select"
            value={selectedDifficulty}
            onChange={(e) =>
              setSelectedDifficulty(
                e.target.value as "easy" | "medium" | "hard"
              )
            }
            className="difficulty-select"
          >
            <option value="easy">Easy (Level 1-3)</option>
            <option value="medium">Medium (Level 4-7)</option>
            <option value="hard">Hard (Level 8-12)</option>
          </select>
        </div>

        <div className="control-buttons">
          <button
            onClick={handleGenerate}
            className="generate-btn"
            disabled={isGenerating}
          >
            {isGenerating ? (
              <>
                <span className="spinner"></span>
                Generating...
              </>
            ) : (
              "🎯 Generate Single Scenario"
            )}
          </button>

          <button
            onClick={handleGenerateMultiple}
            className="generate-multiple-btn"
            disabled={isGenerating}
          >
            {isGenerating ? (
              <>
                <span className="spinner"></span>
                Generating...
              </>
            ) : (
              "🎲 Generate Multiple Scenarios"
            )}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="error-message">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      {/* Generated Scenario Display */}
      {generatedScenario && (
        <div className="generated-scenario">
          <div className="scenario-header">
            <h3>🎭 {generatedScenario.title}</h3>
            <div className="scenario-meta">
              <span className="difficulty-badge difficulty-{generatedScenario.difficulty}">
                {generatedScenario.difficulty.toUpperCase()}
              </span>
              <span className="duration-badge">
                ⏱️ {generatedScenario.estimatedDuration}
              </span>
            </div>
          </div>

          <div className="scenario-setting">
            <h4>🏰 Setting</h4>
            <p>{generatedScenario.setting}</p>
          </div>

          <div className="scenario-npcs">
            <h4>👥 Key NPCs</h4>
            <div className="npcs-grid">
              {generatedScenario.npcs.map((npc, index) => (
                <div key={index} className="npc-card">
                  <div className="npc-name">{npc.name}</div>
                  <div className="npc-role">{npc.role.replace("_", " ")}</div>
                  <div className="npc-personality">
                    {npc.personality.slice(0, 2).join(", ")}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="scenario-scenes">
            <h4>🎬 Adventure Scenes</h4>
            <div className="scenes-list">
              {generatedScenario.scenes.map((scene, index) => (
                <div key={index} className="scene-card">
                  <div className="scene-header">
                    <h5>
                      Scene {index + 1}: {scene.title}
                    </h5>
                    <span className="scene-location">📍 {scene.location}</span>
                  </div>

                  <div className="scene-description">
                    <p>{scene.description}</p>
                  </div>

                  <div className="scene-characters">
                    <strong>Characters:</strong> {scene.characters.join(", ")}
                  </div>

                  <div className="scene-choices">
                    <strong>Player Choices:</strong>
                    <ul>
                      {scene.choices.map((choice, choiceIndex) => (
                        <li key={choiceIndex}>
                          <span className="choice-letter">
                            {String.fromCharCode(65 + choiceIndex)})
                          </span>
                          {choice}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="scene-mechanics">
                    <strong>RPG Mechanics:</strong>
                    <div className="mechanics-tags">
                      {scene.rpgMechanics.map((mechanic, mechIndex) => (
                        <span key={mechIndex} className="mechanic-tag">
                          {mechanic}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {generatedScenario.boss && (
            <div className="scenario-boss">
              <h4>👹 Final Boss</h4>
              <div className="boss-card">
                <div className="boss-name">{generatedScenario.boss.name}</div>
                <div className="boss-role">{generatedScenario.boss.role}</div>
                <div className="boss-description">
                  {generatedScenario.boss.visualDescription}
                </div>
                <div className="boss-stats">
                  <strong>RPG Stats:</strong>
                  <div className="stats-grid">
                    {Object.entries(generatedScenario.boss.rpgStats).map(
                      ([stat, value]) => (
                        <div key={stat} className="stat-item">
                          <span className="stat-name">{stat}:</span>
                          <span className="stat-value">{value}</span>
                        </div>
                      )
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          <div className="scenario-conflicts">
            <h4>⚔️ Major Conflicts</h4>
            <div className="conflicts-list">
              {generatedScenario.conflicts.map((conflict, index) => (
                <div key={index} className="conflict-item">
                  <span className="conflict-icon">⚔️</span>
                  <span className="conflict-text">{conflict}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="scenario-actions">
            <button className="export-btn">📄 Export as PDF</button>
            <button className="save-btn">💾 Save Scenario</button>
            <button className="share-btn">🔗 Share Scenario</button>
          </div>
        </div>
      )}

      {/* Knowledge Base Info */}
      <div className="knowledge-info">
        <h4>🧠 Learning Summary</h4>
        <div className="knowledge-stats">
          <div className="stat">
            <span className="stat-number">
              {knowledgeBase?.storyPatterns.length || 0}
            </span>
            <span className="stat-label">Story Patterns</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {knowledgeBase?.characterArchetypes.length || 0}
            </span>
            <span className="stat-label">Character Types</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {knowledgeBase?.dialogueStyles.length || 0}
            </span>
            <span className="stat-label">Dialogue Styles</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {knowledgeBase?.conflictTypes.length || 0}
            </span>
            <span className="stat-label">Conflict Types</span>
          </div>
        </div>
      </div>
    </div>
  );
};
