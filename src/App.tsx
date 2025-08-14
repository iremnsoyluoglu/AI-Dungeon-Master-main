import React, { useState } from "react";
import "./App.css";
import { GameMasterUI } from "./components/GameMasterUI";
import GameAuthScreen from "./components/GameAuthScreen";
import ScenarioSelectionUI from "./components/ScenarioSelectionUI";

// Default scenario for testing
const defaultScenario = {
  id: "fantasy_dragon",
  title: "Ejderha Avcısının Yolu",
  description: "Fantastik bir dünyada ejderha avı macerası",
  theme: "fantasy",
  difficulty: "hard",
};

function App() {
  const [currentView, setCurrentView] = useState("auth");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [selectedScenario, setSelectedScenario] = useState(null);

  const handleAuthenticated = () => {
    setIsAuthenticated(true);
    setCurrentView("scenario-selection");
  };

  const handleScenarioSelect = async (scenarioId: string) => {
    try {
      // Fetch the actual scenario data from the API
      const response = await fetch(`/api/scenarios`);
      if (response.ok) {
        const data = await response.json();
        const scenario = data.scenarios.find((s: any) => s.id === scenarioId);
        
        if (scenario) {
          setSelectedScenario(scenario);
          setCurrentView("game");
        } else {
          console.error("Scenario not found:", scenarioId);
          // Fallback to default scenario
          setSelectedScenario({
            ...defaultScenario,
            id: scenarioId,
          });
          setCurrentView("game");
        }
      } else {
        console.error("Failed to fetch scenarios");
        // Fallback to default scenario
        setSelectedScenario({
          ...defaultScenario,
          id: scenarioId,
        });
        setCurrentView("game");
      }
    } catch (error) {
      console.error("Error fetching scenario:", error);
      // Fallback to default scenario
      setSelectedScenario({
        ...defaultScenario,
        id: scenarioId,
      });
      setCurrentView("game");
    }
  };

  const handleBackToAuth = () => {
    setCurrentView("auth");
    setIsAuthenticated(false);
    setSelectedScenario(null);
  };

  const handleGameEnd = () => {
    setCurrentView("auth");
    setIsAuthenticated(false);
    setSelectedScenario(null);
  };

  return (
    <div className="App">
      {currentView === "auth" && (
        <GameAuthScreen onAuthenticated={handleAuthenticated} />
      )}

      {currentView === "scenario-selection" && (
        <ScenarioSelectionUI 
          onScenarioSelect={handleScenarioSelect}
          onBack={handleBackToAuth}
        />
      )}

      {currentView === "game" && selectedScenario && (
        <GameMasterUI scenario={selectedScenario} onGameEnd={handleGameEnd} />
      )}
    </div>
  );
}

export default App;
