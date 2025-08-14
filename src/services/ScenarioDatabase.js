const fs = require("fs").promises;
const path = require("path");

class ScenarioDatabase {
  constructor() {
    this.dbPath = path.join(__dirname, "../../data/scenarios.json");
    this.scenarios = [];
  }

  async initialize() {
    try {
      await this.ensureDataDirectory();
      await this.loadScenarios();
    } catch (error) {
      console.warn("Scenario database initialization failed:", error.message);
      this.scenarios = [];
    }
  }

  async ensureDataDirectory() {
    const dataDir = path.dirname(this.dbPath);
    try {
      await fs.access(dataDir);
    } catch {
      await fs.mkdir(dataDir, { recursive: true });
    }
  }

  async loadScenarios() {
    try {
      const data = await fs.readFile(this.dbPath, "utf8");
      this.scenarios = JSON.parse(data);
    } catch (error) {
      console.log("No existing scenarios found, starting with empty database");
      this.scenarios = [];
    }
  }

  async saveScenarios() {
    try {
      await fs.writeFile(this.dbPath, JSON.stringify(this.scenarios, null, 2));
    } catch (error) {
      console.error("Failed to save scenarios:", error);
    }
  }

  async saveScenario(scenario, metadata, tags) {
    const storedScenario = {
      id: Date.now().toString(),
      title: scenario.title,
      theme: scenario.theme,
      difficulty: scenario.difficulty,
      description: scenario.description || `${scenario.theme} temalı macera`,
      isFavorite: false,
      createdAt: new Date().toISOString(),
      tags: tags || [],
      ...metadata,
      ...scenario,
    };

    this.scenarios.unshift(storedScenario);
    await this.saveScenarios();
    return storedScenario;
  }

  async getAllScenarios() {
    return this.scenarios;
  }

  async getFavorites() {
    return this.scenarios.filter((s) => s.isFavorite);
  }

  async toggleFavorite(scenarioId) {
    const scenario = this.scenarios.find((s) => s.id === scenarioId);
    if (scenario) {
      scenario.isFavorite = !scenario.isFavorite;
      await this.saveScenarios();
      return scenario.isFavorite;
    }
    return false;
  }

  async searchScenarios(query, filters = {}) {
    let results = this.scenarios;

    // Text search
    if (query) {
      const searchTerm = query.toLowerCase();
      results = results.filter(
        (s) =>
          s.title.toLowerCase().includes(searchTerm) ||
          s.description.toLowerCase().includes(searchTerm) ||
          s.tags.some((tag) => tag.toLowerCase().includes(searchTerm))
      );
    }

    // Filter by theme
    if (filters.theme) {
      results = results.filter((s) => s.theme === filters.theme);
    }

    // Filter by difficulty
    if (filters.difficulty) {
      results = results.filter((s) => s.difficulty === filters.difficulty);
    }

    // Filter by favorites
    if (filters.favoritesOnly) {
      results = results.filter((s) => s.isFavorite);
    }

    return results;
  }

  async getScenarioById(scenarioId) {
    return this.scenarios.find((s) => s.id === scenarioId);
  }

  async deleteScenario(scenarioId) {
    const index = this.scenarios.findIndex((s) => s.id === scenarioId);
    if (index !== -1) {
      this.scenarios.splice(index, 1);
      await this.saveScenarios();
      return true;
    }
    return false;
  }

  getStats() {
    const total = this.scenarios.length;
    const favorites = this.scenarios.filter((s) => s.isFavorite).length;
    const themes = [...new Set(this.scenarios.map((s) => s.theme))];
    const difficulties = [...new Set(this.scenarios.map((s) => s.difficulty))];

    return {
      total,
      favorites,
      themes,
      difficulties,
      averageGenerationTime:
        this.scenarios.length > 0
          ? this.scenarios.reduce(
              (sum, s) => sum + (s.generationTime || 0),
              0
            ) / this.scenarios.length
          : 0,
    };
  }
}

module.exports = { ScenarioDatabase };
