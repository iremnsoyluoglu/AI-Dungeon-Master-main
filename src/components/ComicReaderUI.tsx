import React, { useState, useEffect } from "react";
import { GetComicsReader } from "../services/GetComicsReader";
import { ComicLearningEngine } from "../services/ComicLearningEngine";
import { LearnedScenarioGenerator } from "../services/LearnedScenarioGenerator";
import {
  ComicIssue,
  LearnedPatterns,
  RPGScenario,
  ScenarioKnowledge,
} from "../types/comic";
import "./ComicReaderUI.css";

interface ReadComic {
  title: string;
  learnedPatterns: LearnedPatterns;
  progress: number;
}

interface ComicReaderUIProps {
  onKnowledgeBaseUpdate?: (knowledge: ScenarioKnowledge) => void;
}

export const ComicReaderUI: React.FC<ComicReaderUIProps> = ({
  onKnowledgeBaseUpdate,
}) => {
  const [selectedGenre, setSelectedGenre] = useState<string>("fantasy");
  const [readComics, setReadComics] = useState<ReadComic[]>([]);
  const [learningProgress, setLearningProgress] = useState<number>(0);
  const [knowledgeBase, setKnowledgeBase] = useState<ScenarioKnowledge | null>(
    null
  );
  const [isLearning, setIsLearning] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleStartReading = async () => {
    setIsLearning(true);
    setError(null);
    setLearningProgress(0);
    setReadComics([]);

    try {
      const reader = new GetComicsReader();
      const learningEngine = new ComicLearningEngine();

      console.log(`Starting to read ${selectedGenre} comics...`);

      // Fetch comics by genre
      const comics = await reader.fetchComicsByGenre(selectedGenre, 5); // Limit to 5 for demo

      console.log(`Found ${comics.length} comics to process`);

      // Process each comic and learn patterns
      for (let i = 0; i < comics.length; i++) {
        const comic = comics[i];

        try {
          console.log(
            `Processing comic ${i + 1}/${comics.length}: ${comic.title}`
          );

          const learnedPatterns = await learningEngine.processComic(comic);

          setReadComics((prev) => [
            ...prev,
            {
              title: comic.title,
              learnedPatterns: learnedPatterns,
              progress: 100,
            },
          ]);

          setLearningProgress(((i + 1) / comics.length) * 100);

          // Add delay to show progress
          await new Promise((resolve) => setTimeout(resolve, 1000));
        } catch (error) {
          console.error(`Error processing comic ${comic.title}:`, error);
          setError(`Failed to process ${comic.title}: ${error}`);
          continue;
        }
      }

      // Get final knowledge base
      const finalKnowledge = learningEngine.getKnowledgeBase();
      setKnowledgeBase(finalKnowledge);

      // Notify parent component
      if (onKnowledgeBaseUpdate) {
        onKnowledgeBaseUpdate(finalKnowledge);
      }

      console.log("Learning completed!", finalKnowledge);
    } catch (error) {
      console.error("Error during learning process:", error);
      setError(`Learning failed: ${error}`);
    } finally {
      setIsLearning(false);
    }
  };

  const handleGenerateScenario = () => {
    if (!knowledgeBase) {
      setError("Please complete the comic reading process first!");
      return;
    }

    // This will be handled by the scenario generator component
    console.log("Scenario generation requested");
  };

  return (
    <div className="comic-reader">
      <div className="header">
        <h1>🎭 Comic Reading & Learning System</h1>
        <p>Read comics from GetComics and learn RPG scenario patterns</p>
      </div>

      <div className="main-content">
        {/* Genre Selection */}
        <div className="genre-selection">
          <h2>Choose Your Learning Genre</h2>
          <div className="genre-grid">
            {[
              {
                value: "fantasy",
                label: "Fantasy",
                icon: "⚔️",
                desc: "D&D, Conan, LotR comics",
              },
              {
                value: "sci-fi",
                label: "Sci-Fi",
                icon: "🚀",
                desc: "40K, Star Wars, Alien comics",
              },
              {
                value: "horror",
                label: "Horror",
                icon: "👻",
                desc: "Hellboy, Constantine, zombie comics",
              },
              {
                value: "adventure",
                label: "Adventure",
                icon: "🗺️",
                desc: "Indiana Jones style",
              },
              {
                value: "superhero",
                label: "Superhero",
                icon: "🦸",
                desc: "Marvel, DC comics",
              },
            ].map((genre) => (
              <div
                key={genre.value}
                className={`genre-card ${
                  selectedGenre === genre.value ? "selected" : ""
                }`}
                onClick={() => setSelectedGenre(genre.value)}
              >
                <div className="genre-icon">{genre.icon}</div>
                <div className="genre-label">{genre.label}</div>
                <div className="genre-desc">{genre.desc}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Start Reading Button */}
        <div className="action-section">
          <button
            onClick={handleStartReading}
            className="start-reading-btn"
            disabled={isLearning}
          >
            {isLearning ? (
              <>
                <span className="spinner"></span>
                Learning from Comics...
              </>
            ) : (
              <>📚 Start Reading & Learning</>
            )}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="error-message">
            <span>⚠️ {error}</span>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        {/* Progress Bar */}
        {learningProgress > 0 && (
          <div className="progress-section">
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${learningProgress}%` }}
              ></div>
            </div>
            <div className="progress-text">
              Learning Progress: {Math.round(learningProgress)}%
            </div>
          </div>
        )}

        {/* Read Comics List */}
        {readComics.length > 0 && (
          <div className="read-comics">
            <h2>📖 Comics Processed</h2>
            <div className="comics-grid">
              {readComics.map((comic, index) => (
                <div key={index} className="comic-item">
                  <div className="comic-header">
                    <h3>{comic.title}</h3>
                    <div className="comic-progress">
                      <div className="progress-circle">
                        <span>{comic.progress}%</span>
                      </div>
                    </div>
                  </div>

                  <div className="comic-stats">
                    <div className="stat">
                      <span className="stat-label">Story Patterns:</span>
                      <span className="stat-value">
                        {comic.learnedPatterns.storyFlow.length}
                      </span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Characters:</span>
                      <span className="stat-value">
                        {comic.learnedPatterns.characters.length}
                      </span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Dialogue Styles:</span>
                      <span className="stat-value">
                        {comic.learnedPatterns.dialogue.length}
                      </span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Action Sequences:</span>
                      <span className="stat-value">
                        {comic.learnedPatterns.actionSequences.length}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Knowledge Base Summary */}
        {knowledgeBase && (
          <div className="knowledge-summary">
            <h2>🧠 Learned Knowledge Base</h2>
            <div className="knowledge-grid">
              <div className="knowledge-card">
                <div className="knowledge-icon">📚</div>
                <div className="knowledge-title">Story Patterns</div>
                <div className="knowledge-count">
                  {knowledgeBase.storyPatterns.length}
                </div>
              </div>
              <div className="knowledge-card">
                <div className="knowledge-icon">👥</div>
                <div className="knowledge-title">Character Types</div>
                <div className="knowledge-count">
                  {knowledgeBase.characterArchetypes.length}
                </div>
              </div>
              <div className="knowledge-card">
                <div className="knowledge-icon">💬</div>
                <div className="knowledge-title">Dialogue Styles</div>
                <div className="knowledge-count">
                  {knowledgeBase.dialogueStyles.length}
                </div>
              </div>
              <div className="knowledge-card">
                <div className="knowledge-icon">⚔️</div>
                <div className="knowledge-title">Conflict Types</div>
                <div className="knowledge-count">
                  {knowledgeBase.conflictTypes.length}
                </div>
              </div>
            </div>

            <div className="scenario-generation">
              <h3>🎲 Ready to Generate RPG Scenarios!</h3>
              <p>
                Your AI has learned from {readComics.length} comics and is ready
                to create unique RPG adventures.
              </p>
              <button
                onClick={handleGenerateScenario}
                className="generate-scenario-btn"
              >
                🎯 Generate RPG Scenario
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
