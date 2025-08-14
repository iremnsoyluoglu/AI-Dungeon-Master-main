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
} from "@mui/icons-material";

const CharacterPanel = ({ character }) => {
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

  return (
    <Box sx={{ p: 2, color: "white" }}>
      {/* Karakter Başlığı */}
      <Typography
        variant="h5"
        sx={{ color: "#ffc107", mb: 2, textAlign: "center" }}
      >
        👤 {character.name}
      </Typography>

      {/* Sınıf ve Seviye */}
      <Paper
        elevation={2}
        sx={{
          p: 2,
          mb: 2,
          backgroundColor: "rgba(255,193,7,0.1)",
          border: "1px solid #ffc107",
        }}
      >
        <Typography variant="h6" sx={{ color: "#ffc107", mb: 1 }}>
          ⚔️ {character.class}
        </Typography>
        <Typography variant="body2" sx={{ color: "white" }}>
          Seviye: {character.level}
        </Typography>
        <Typography variant="body2" sx={{ color: "white" }}>
          Faction: {character.faction}
        </Typography>
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

      {/* Yetenekler */}
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
          🧙 Yetenekler
        </Typography>
        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
          <Chip
            label="Fire Magic"
            size="small"
            sx={{
              backgroundColor: "#f44336",
              color: "white",
              fontSize: "0.7rem",
            }}
          />
          <Chip
            label="Ice Magic"
            size="small"
            sx={{
              backgroundColor: "#2196f3",
              color: "white",
              fontSize: "0.7rem",
            }}
          />
          <Chip
            label="Arcane Shield"
            size="small"
            sx={{
              backgroundColor: "#9c27b0",
              color: "white",
              fontSize: "0.7rem",
            }}
          />
        </Box>
      </Paper>

      {/* Envanter */}
      <Paper
        elevation={2}
        sx={{
          p: 2,
          backgroundColor: "rgba(76,175,80,0.1)",
          border: "1px solid #4caf50",
        }}
      >
        <Typography variant="h6" sx={{ color: "#4caf50", mb: 1 }}>
          🎒 Envanter
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
            label="Health Potion"
            size="small"
            sx={{
              backgroundColor: "#f44336",
              color: "white",
              fontSize: "0.7rem",
            }}
          />
        </Box>
      </Paper>
    </Box>
  );
};

export default CharacterPanel;
