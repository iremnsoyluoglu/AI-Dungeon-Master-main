import React from "react";
import {
  Box,
  Typography,
  LinearProgress,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Paper,
} from "@mui/material";
import {
  Favorite,
  Security,
  Star,
  MonetizationOn,
  Inventory,
  Shield,
  SportsMartialArts,
  LocationOn,
  Psychology,
} from "@mui/icons-material";

const StatsPanel = ({ character, gameState }) => {
  const stats = [
    {
      name: "Can",
      value: character.health,
      max: character.maxHealth,
      icon: <Favorite />,
      color: "#f44336",
    },
    {
      name: "Mana",
      value: character.mana,
      max: character.maxMana,
      icon: <Security />,
      color: "#2196f3",
    },
    {
      name: "Deneyim",
      value: character.experience,
      max: character.level * 100,
      icon: <Star />,
      color: "#ffc107",
    },
  ];

  const attributes = [
    { name: "Güç", value: character.stats.strength, icon: <SportsMartialArts /> },
    { name: "Çeviklik", value: character.stats.dexterity, icon: <Shield /> },
    { name: "Zeka", value: character.stats.intelligence, icon: <Star /> },
    {
      name: "Dayanıklılık",
      value: character.stats.constitution,
      icon: <Favorite />,
    },
    { name: "Bilgelik", value: character.stats.wisdom, icon: <Security /> },
    {
      name: "Karizma",
      value: character.stats.charisma,
      icon: <MonetizationOn />,
    },
  ];

  const gameInfo = gameState?.player || {};
  const storyInfo = gameState?.story || {};

  return (
    <Box sx={{ p: 2, color: "white" }}>
      {/* Oyun Durumu */}
      <Paper
        elevation={2}
        sx={{
          p: 2,
          mb: 2,
          backgroundColor: "rgba(255,255,255,0.05)",
          border: "1px solid #ff9800",
        }}
      >
        <Typography variant="h6" sx={{ mb: 1, color: "#ff9800" }}>
          🎮 Oyun Durumu
        </Typography>
        <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
          <LocationOn sx={{ color: "#4caf50", mr: 1 }} />
          <Typography variant="body2" sx={{ color: "white" }}>
            Konum: {gameInfo.location || "Bilinmiyor"}
          </Typography>
        </Box>
        <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
          <Psychology sx={{ color: "#9c27b0", mr: 1 }} />
          <Typography variant="body2" sx={{ color: "white" }}>
            Karma: {gameInfo.karma || 0}
          </Typography>
        </Box>
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <Star sx={{ color: "#ffc107", mr: 1 }} />
          <Typography variant="body2" sx={{ color: "white" }}>
            Ziyaret Edilen: {storyInfo.visitedScenes?.length || 0} sahne
          </Typography>
        </Box>
      </Paper>

      {/* Temel İstatistikler */}
      <Paper
        elevation={2}
        sx={{
          p: 2,
          mb: 2,
          backgroundColor: "rgba(76,175,80,0.1)",
          border: "1px solid #4caf50",
        }}
      >
        <Typography variant="h6" sx={{ color: "#4caf50", mb: 1 }}>
          📊 Temel İstatistikler
        </Typography>
        {stats.map((stat, index) => (
          <Box key={index} sx={{ mb: 1 }}>
            <Box sx={{ display: "flex", alignItems: "center", mb: 0.5 }}>
              <Box sx={{ color: stat.color, mr: 1 }}>{stat.icon}</Box>
              <Typography variant="body2" sx={{ color: "white", flex: 1 }}>
                {stat.name}
              </Typography>
              <Typography variant="body2" sx={{ color: "white" }}>
                {stat.value}/{stat.max}
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={(stat.value / stat.max) * 100}
              sx={{
                height: 6,
                borderRadius: 3,
                backgroundColor: "rgba(255,255,255,0.1)",
                "& .MuiLinearProgress-bar": { backgroundColor: stat.color },
              }}
            />
          </Box>
        ))}
      </Paper>

      <Divider sx={{ borderColor: "#ffc107", my: 2 }} />

      {/* Özellikler */}
      <Paper
        elevation={2}
        sx={{
          p: 2,
          mb: 2,
          backgroundColor: "rgba(156,39,176,0.1)",
          border: "1px solid #9c27b0",
        }}
      >
        <Typography variant="h6" sx={{ color: "#9c27b0", mb: 1 }}>
          🎯 Özellikler
        </Typography>
        <List dense>
          {attributes.map((attr, index) => (
            <ListItem key={index} sx={{ px: 0 }}>
              <ListItemIcon sx={{ color: "#9c27b0", minWidth: 30 }}>
                {attr.icon}
              </ListItemIcon>
              <ListItemText
                primary={attr.name}
                secondary={attr.value}
                sx={{
                  "& .MuiListItemText-primary": {
                    color: "white",
                    fontSize: "0.9rem",
                  },
                  "& .MuiListItemText-secondary": {
                    color: "#8b949e",
                    fontSize: "0.8rem",
                  },
                }}
              />
            </ListItem>
          ))}
        </List>
      </Paper>

      {/* Ekipman */}
      <Paper
        elevation={2}
        sx={{
          p: 2,
          mb: 2,
          backgroundColor: "rgba(255,152,0,0.1)",
          border: "1px solid #ff9800",
        }}
      >
        <Typography variant="h6" sx={{ color: "#ff9800", mb: 1 }}>
          ⚔️ Ekipman
        </Typography>
        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
          <Chip
            label="Steel Sword"
            size="small"
            sx={{ backgroundColor: "#666", color: "white", fontSize: "0.7rem" }}
          />
          <Chip
            label="Leather Armor"
            size="small"
            sx={{ backgroundColor: "#666", color: "white", fontSize: "0.7rem" }}
          />
          <Chip
            label="Magic Ring"
            size="small"
            sx={{
              backgroundColor: "#9c27b0",
              color: "white",
              fontSize: "0.7rem",
            }}
          />
        </Box>
      </Paper>

      {/* Hızlı Bilgi */}
      <Paper
        elevation={2}
        sx={{
          p: 2,
          backgroundColor: "rgba(76,175,80,0.1)",
          border: "1px solid #4caf50",
        }}
      >
        <Typography variant="h6" sx={{ color: "#4caf50", mb: 1 }}>
          ⚡ Hızlı Bilgi
        </Typography>
        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
          <Chip
            label="Aktif Görev: 3"
            size="small"
            sx={{
              backgroundColor: "#4caf50",
              color: "white",
              fontSize: "0.7rem",
            }}
          />
          <Chip
            label="Tamamlanan: 7"
            size="small"
            sx={{ backgroundColor: "#666", color: "white", fontSize: "0.7rem" }}
          />
          <Chip
            label="Seviye: 5"
            size="small"
            sx={{
              backgroundColor: "#ffc107",
              color: "black",
              fontSize: "0.7rem",
            }}
          />
        </Box>
      </Paper>

      {/* Hikaye Bayrakları */}
      {storyInfo.storyFlags && Object.keys(storyInfo.storyFlags).length > 0 && (
        <Box sx={{ mt: 2 }}>
          <Typography
            variant="caption"
            sx={{ color: "#ff9800", display: "block", mb: 1 }}
          >
            Hikaye Bayrakları:
          </Typography>
          <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
            {Object.entries(storyInfo.storyFlags).map(([flag, value]) => (
              <Chip
                key={flag}
                label={flag}
                size="small"
                sx={{
                  backgroundColor: value ? "#4caf50" : "#666",
                  color: "white",
                  fontSize: "0.7rem",
                }}
              />
            ))}
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default StatsPanel;
