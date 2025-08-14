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

  const handleGenerate = () => {
    if (!knowledgeBase) {
      setError("Please complete the comic reading process first!");
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      const generator = new LearnedScenarioGenerator(knowledgeBase);
      const scenario = generator.generateRPGScenario(
        selectedTheme,
        selectedDifficulty
      );

      setGeneratedScenario(scenario);
      console.log("Generated scenario:", scenario);
    } catch (error) {
      console.error("Error generating scenario:", error);
      setError(`Failed to generate scenario: ${error}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleGenerateMultiple = () => {
    if (!knowledgeBase) {
      setError("Please complete the comic reading process first!");
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      const generator = new LearnedScenarioGenerator(knowledgeBase);
      const scenarios = generator.generateMultipleScenarios(selectedTheme, 3);

      // For now, just show the first one
      setGeneratedScenario(scenarios[0]);
      console.log("Generated multiple scenarios:", scenarios);
    } catch (error) {
      console.error("Error generating scenarios:", error);
      setError(`Failed to generate scenarios: ${error}`);
    } finally {
      setIsGenerating(false);
    }
  };

  if (!knowledgeBase) {
    return (
      <div className="scenario-generator">
        <div className="no-knowledge">
          <h2>🎲 Scenario Generator</h2>
          <p>
            Please complete the comic reading process first to generate RPG
            scenarios.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="scenario-generator">
      <div className="generator-header">
        <h2>🎲 Generate RPG Scenarios from Learned Patterns</h2>
        <p>Create unique adventures based on comic storytelling techniques</p>
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
              {knowledgeBase.storyPatterns.length}
            </span>
            <span className="stat-label">Story Patterns</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {knowledgeBase.characterArchetypes.length}
            </span>
            <span className="stat-label">Character Types</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {knowledgeBase.dialogueStyles.length}
            </span>
            <span className="stat-label">Dialogue Styles</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {knowledgeBase.conflictTypes.length}
            </span>
            <span className="stat-label">Conflict Types</span>
          </div>
        </div>
      </div>
    </div>
  );
};
