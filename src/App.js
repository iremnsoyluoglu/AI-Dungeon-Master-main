import React, { useState } from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { CssBaseline, Box } from "@mui/material";
import GameLayout from "./components/GameLayout";
import GameAuthScreen from "./components/GameAuthScreen";
import { GameStateManager } from "./components/GameStateManager";

const warhammerTheme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#ffc107" }, // Imperial Gold
    secondary: { main: "#4caf50" }, // Imperial Green
    background: {
      default: "#0d1117",
      paper: "#1c2128",
    },
    text: {
      primary: "#ffffff",
      secondary: "#8b949e",
    },
  },
  typography: {
    fontFamily: '"Orbitron", "Roboto", monospace',
    h5: { fontWeight: 700 },
    h6: { fontWeight: 600 },
  },
});

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [gameManager] = useState(() => new GameStateManager());
  const [gameState, setGameState] = useState(gameManager.getGameState());

  const [character, setCharacter] = useState({
    name: "Commissar Yarrick",
    class: "Imperial Guard",
    level: gameState.player.level,
    health: gameState.player.health,
    maxHealth: 100,
    mana: gameState.player.mana,
    maxMana: 50,
    experience: gameState.player.experience,
    faction: "Cadia",
    stats: {
      strength: 16,
      dexterity: 12,
      intelligence: 14,
      constitution: 15,
      wisdom: 13,
      charisma: 11,
    },
  });

  const handleAction = (actionType, customText) => {
    console.log("Action:", actionType, customText);

    // Aksiyon sonuçlarını işle
    switch (actionType) {
      case "combat":
        console.log("Savaş aksiyonu gerçekleştirildi");
        break;
      case "talk":
        console.log("Konuşma aksiyonu gerçekleştirildi");
        break;
      case "investigate":
        console.log("İnceleme aksiyonu gerçekleştirildi");
        break;
      case "flee":
        console.log("Kaçma aksiyonu gerçekleştirildi");
        break;
      case "inventory":
        console.log("Envanter aksiyonu gerçekleştirildi");
        break;
      case "cast_spell":
        console.log("Büyü aksiyonu gerçekleştirildi");
        break;
      case "custom":
        console.log("Özel aksiyon:", customText);
        break;
      case "choice_result":
        console.log("Seçim sonucu:", customText);
        break;
      default:
        console.log("Bilinmeyen aksiyon:", actionType);
    }
  };

  const handleGameStateUpdate = (newGameState) => {
    setGameState(newGameState);

    // Karakter durumunu güncelle
    setCharacter((prev) => ({
      ...prev,
      level: newGameState.player.level,
      health: newGameState.player.health,
      mana: newGameState.player.mana,
      experience: newGameState.player.experience,
    }));
  };

  const handleAuthenticated = () => {
    setIsAuthenticated(true);
  };

  return (
    <ThemeProvider theme={warhammerTheme}>
      <CssBaseline />
      <Box sx={{ height: "100vh", overflow: "hidden" }}>
        {isAuthenticated ? (
          <GameLayout
            character={character}
            gameState={gameState}
            onAction={handleAction}
            onGameStateUpdate={handleGameStateUpdate}
          />
        ) : (
          <GameAuthScreen onAuthenticated={handleAuthenticated} />
        )}
      </Box>
    </ThemeProvider>
  );
}

export default App;
