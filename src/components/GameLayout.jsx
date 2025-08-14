import React from "react";
import { Grid, Paper } from "@mui/material";
import CharacterPanel from "./CharacterPanel";
import StoryPanel from "./StoryPanel";
import StatsPanel from "./StatsPanel";

const GameLayout = ({ character, gameState, onAction, onGameStateUpdate }) => {
  return (
    <Grid container sx={{ height: "100vh" }} spacing={0.5}>
      {/* SOL PANEL - Skills */}
      <Grid item xs={3}>
        <Paper
          elevation={4}
          sx={{
            height: "100vh",
            overflow: "auto",
            background:
              "linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%)",
            border: "2px solid #4caf50",
            borderRadius: "8px 0 0 8px",
          }}
        >
          <CharacterPanel character={character} />
        </Paper>
      </Grid>

      {/* ORTA PANEL - Story */}
      <Grid item xs={6}>
        <Paper
          elevation={4}
          sx={{
            height: "100vh",
            background:
              "linear-gradient(135deg, #263238 0%, #37474f 50%, #455a64 100%)",
            border: "2px solid #ffc107",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <StoryPanel
            gameState={gameState}
            onAction={onAction}
            onGameStateUpdate={onGameStateUpdate}
          />
        </Paper>
      </Grid>

      {/* SAĞ PANEL - Stats */}
      <Grid item xs={3}>
        <Paper
          elevation={4}
          sx={{
            height: "100vh",
            overflow: "auto",
            background:
              "linear-gradient(135deg, #4a148c 0%, #6a1b9a 50%, #7b1fa2 100%)",
            border: "2px solid #ff9800",
            borderRadius: "0 8px 8px 0",
          }}
        >
          <StatsPanel character={character} gameState={gameState} />
        </Paper>
      </Grid>
    </Grid>
  );
};

export default GameLayout;
