import React, { useState, useEffect } from "react";
import "./ScenarioSelectionUI.css";

interface Scenario {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  estimatedPlayTime: number;
  theme: string;
  genre: string;
  complexity: string;
  is_favorite?: boolean;
}

interface ScenarioSelectionUIProps {
  onScenarioSelect: (scenarioId: string) => void;
  onBack: () => void;
}

const ScenarioSelectionUI: React.FC<ScenarioSelectionUIProps> = ({
  onScenarioSelect,
  onBack,
}) => {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [filteredScenarios, setFilteredScenarios] = useState<Scenario[]>([]);
  const [selectedTheme, setSelectedTheme] = useState<string>("");
  const [searchTerm, setSearchTerm] = useState("");
  const [difficultyFilter, setDifficultyFilter] = useState<string>("");
  const [showFavorites, setShowFavorites] = useState(false);
  const [loading, setLoading] = useState(true);

  const themes = [
    {
      id: "fantasy",
      name: "🎭 Fantasy",
      description: "Ejderhalar, büyücüler ve büyülü dünyalar",
    },
    {
      id: "warhammer40k",
      name: "⚔️ Warhammer 40K",
      description: "Uzay savaşları, orklar ve İmparatorluk",
    },
    {
      id: "cyberpunk",
      name: "🌆 Cyberpunk",
      description: "Neon ışıkları, AI ve mega şirketler",
    },
  ];

  useEffect(() => {
    loadScenarios();
  }, []);

  useEffect(() => {
    filterScenarios();
  }, [scenarios, selectedTheme, searchTerm, difficultyFilter, showFavorites]);

  const loadScenarios = async () => {
    try {
      const response = await fetch("/api/scenarios");
      if (response.ok) {
        const data = await response.json();
        console.log("API Response:", data);

        // API'den gelen veriyi doğru şekilde işle
        if (data.success && data.scenarios) {
          setScenarios(data.scenarios);
        } else if (Array.isArray(data)) {
          setScenarios(data);
        } else {
          console.error("Unexpected API response format:", data);
        }
      }
    } catch (error) {
      console.error("Error loading scenarios:", error);
    } finally {
      setLoading(false);
    }
  };

  const filterScenarios = () => {
    let filtered = scenarios;

    // Filter by theme
    if (selectedTheme) {
      filtered = filtered.filter(
        (scenario) => scenario.theme === selectedTheme
      );
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(
        (scenario) =>
          scenario.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
          scenario.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by difficulty
    if (difficultyFilter) {
      filtered = filtered.filter(
        (scenario) => scenario.difficulty === difficultyFilter
      );
    }

    // Filter by favorites
    if (showFavorites) {
      filtered = filtered.filter((scenario) => scenario.is_favorite);
    }

    setFilteredScenarios(filtered);
  };

  const handleThemeSelect = (theme: string) => {
    setSelectedTheme(theme);
  };

  const handleFavoriteToggle = async (scenarioId: string) => {
    try {
      // Toggle favorite status
      const response = await fetch(
        `/api/scenarios/${scenarioId}/toggle-favorite`,
        {
          method: "POST",
        }
      );
      if (response.ok) {
        // Update local state
        setScenarios((prev) =>
          prev.map((scenario) =>
            scenario.id === scenarioId
              ? { ...scenario, is_favorite: !scenario.is_favorite }
              : scenario
          )
        );
      }
    } catch (error) {
      console.error("Error toggling favorite:", error);
    }
  };

  const handleScenarioSelect = (scenarioId: string) => {
    onScenarioSelect(scenarioId);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "easy":
        return "#4CAF50";
      case "medium":
        return "#FF9800";
      case "hard":
        return "#F44336";
      default:
        return "#757575";
    }
  };

  const getThemeIcon = (theme: string) => {
    switch (theme) {
      case "fantasy":
        return "🐉";
      case "warhammer40k":
        return "⚔️";
      case "cyberpunk":
        return "🌆";
      default:
        return "🎮";
    }
  };

  if (loading) {
    return (
      <div className="scenario-selection-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Senaryolar yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="scenario-selection-container">
      <div className="scenario-header">
        <button className="back-button" onClick={onBack}>
          ← Geri
        </button>
        <h1>🎮 Senaryo Seçimi</h1>
        <p>Önce bir tema seç, sonra senaryonu belirle!</p>
      </div>

      {/* Theme Selection */}
      {!selectedTheme && (
        <div className="theme-selection">
          <h2>🎭 Tema Seçimi</h2>
          <div className="theme-grid">
            {themes.map((theme) => (
              <div
                key={theme.id}
                className="theme-card"
                onClick={() => handleThemeSelect(theme.id)}
              >
                <div className="theme-icon">{theme.name.split(" ")[0]}</div>
                <h3>{theme.name.split(" ").slice(1).join(" ")}</h3>
                <p>{theme.description}</p>
                <div className="theme-scenario-count">
                  {scenarios.filter((s) => s.theme === theme.id).length} Senaryo
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Scenario Selection */}
      {selectedTheme && (
        <div className="scenario-selection">
          <div className="selection-header">
            <button
              className="theme-back-button"
              onClick={() => setSelectedTheme("")}
            >
              ← Tema Seçimine Dön
            </button>
            <h2>
              {themes.find((t) => t.id === selectedTheme)?.name} Senaryoları
            </h2>
          </div>

          {/* Filters */}
          <div className="scenario-filters">
            <div className="filter-group">
              <input
                type="text"
                placeholder="Senaryo ara..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>
            <div className="filter-group">
              <select
                value={difficultyFilter}
                onChange={(e) => setDifficultyFilter(e.target.value)}
                className="difficulty-filter"
              >
                <option value="">Tüm Zorluklar</option>
                <option value="easy">Kolay</option>
                <option value="medium">Orta</option>
                <option value="hard">Zor</option>
              </select>
            </div>
            <div className="filter-group">
              <label className="favorite-checkbox">
                <input
                  type="checkbox"
                  checked={showFavorites}
                  onChange={(e) => setShowFavorites(e.target.checked)}
                />
                Sadece Favoriler
              </label>
            </div>
          </div>

          {/* Scenarios Grid */}
          <div className="scenarios-grid">
            {filteredScenarios.length === 0 ? (
              <div className="no-scenarios">
                <p>Bu temada senaryo bulunamadı.</p>
                <button onClick={() => setSelectedTheme("")}>
                  Başka Tema Seç
                </button>
              </div>
            ) : (
              filteredScenarios.map((scenario) => (
                <div key={scenario.id} className="scenario-card">
                  <div className="scenario-header-card">
                    <div className="scenario-icon">
                      {getThemeIcon(scenario.theme)}
                    </div>
                    <div className="scenario-info">
                      <h3>{scenario.title}</h3>
                      <div className="scenario-meta">
                        <span
                          className="difficulty-badge"
                          style={{
                            backgroundColor: getDifficultyColor(
                              scenario.difficulty
                            ),
                          }}
                        >
                          {scenario.difficulty === "easy"
                            ? "Kolay"
                            : scenario.difficulty === "medium"
                            ? "Orta"
                            : "Zor"}
                        </span>
                        <span className="playtime">
                          ⏱️ {scenario.estimatedPlayTime} dk
                        </span>
                        <span className="complexity">
                          📊{" "}
                          {scenario.complexity === "high" ? "Yüksek" : "Orta"}
                        </span>
                      </div>
                    </div>
                    <button
                      className={`favorite-button ${
                        scenario.is_favorite ? "favorited" : ""
                      }`}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleFavoriteToggle(scenario.id);
                      }}
                    >
                      {scenario.is_favorite ? "❤️" : "🤍"}
                    </button>
                  </div>
                  <p className="scenario-description">{scenario.description}</p>
                  <button
                    className="select-scenario-button"
                    onClick={() => onScenarioSelect(scenario.id)}
                  >
                    Bu Senaryoyu Seç
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ScenarioSelectionUI;
