import React, { useState, useMemo } from "react";
import "./CharacterSelectionUI.css";

interface CharacterClass {
  id: string;
  name: string;
  description: string;
  base_hp: number;
  base_attack: number;
  base_defense: number;
  base_special: number;
  special_abilities: string[];
  starting_equipment: string[];
  base_stats: {
    strength: number;
    dexterity: number;
    constitution: number;
    intelligence: number;
    wisdom: number;
    charisma: number;
  };
  theme: string;
  role: string;
}

interface CharacterRace {
  id: string;
  name: string;
  description: string;
  hp_bonus: number;
  attack_bonus: number;
  defense_bonus: number;
  special_traits: string[];
}

interface CharacterSelectionUIProps {
  characterClasses: { [key: string]: CharacterClass };
  characterRaces: { [key: string]: CharacterRace };
  onCharacterCreate: (characterData: {
    name: string;
    characterClass: string;
    characterRace: string;
  }) => void;
  isLoading: boolean;
  onStartGame: () => void;
}

const CharacterSelectionUI: React.FC<CharacterSelectionUIProps> = ({
  characterClasses,
  characterRaces,
  onCharacterCreate,
  isLoading,
  onStartGame,
}) => {
  const [selectedTheme, setSelectedTheme] = useState("all");
  const [selectedRole, setSelectedRole] = useState("all");
  const [selectedClass, setSelectedClass] = useState<string | null>(null);
  const [selectedRace, setSelectedRace] = useState<string | null>(null);
  const [characterName, setCharacterName] = useState("");
  const [showDetails, setShowDetails] = useState<string | null>(null);

  // Tema ve rol filtreleri
  const themes = useMemo(() => {
    const themeSet = new Set(Object.values(characterClasses).map(cls => cls.theme));
    return Array.from(themeSet);
  }, [characterClasses]);

  const roles = useMemo(() => {
    const roleSet = new Set(Object.values(characterClasses).map(cls => cls.role));
    return Array.from(roleSet);
  }, [characterClasses]);

  // Filtrelenmiş sınıflar
  const filteredClasses = useMemo(() => {
    return Object.entries(characterClasses).filter(([id, charClass]) => {
      const matchesTheme = selectedTheme === "all" || charClass.theme === selectedTheme;
      const matchesRole = selectedRole === "all" || charClass.role === selectedRole;
      return matchesTheme && matchesRole;
    });
  }, [characterClasses, selectedTheme, selectedRole]);

  // Sınıf ikonları
  const getClassIcon = (className: string) => {
    const iconMap: { [key: string]: string } = {
      warrior: "⚔️",
      mage: "🔮",
      rogue: "🗡️",
      priest: "⛪",
      paladin: "🛡️",
      druid: "🌿",
      hunter: "🏹",
      warlock: "👹",
      space_marine: "🛡️",
      tech_priest: "⚙️",
      inquisitor: "🔍",
      imperial_guard: "🎖️",
    };
    return iconMap[className] || "👤";
  };

  // Rol renkleri
  const getRoleColor = (role: string) => {
    const colors: { [key: string]: string } = {
      tank: "#4A90E2",
      damage_dealer: "#E74C3C",
      support: "#27AE60",
      balanced: "#F39C12",
    };
    return colors[role] || "#666";
  };

  // Tema renkleri
  const getThemeColor = (theme: string) => {
    const colors: { [key: string]: string } = {
      fantasy: "#8B4513",
      warhammer40k: "#2C3E50",
    };
    return colors[theme] || "#666";
  };

  // Karakter oluşturma
  const handleCreateCharacter = () => {
    if (!selectedClass || !selectedRace || !characterName.trim()) {
      alert("Lütfen tüm alanları doldurun!");
      return;
    }

    onCharacterCreate({
      name: characterName.trim(),
      characterClass: selectedClass,
      characterRace: selectedRace,
    });
  };

  // Seçili sınıfın detayları
  const selectedClassData = selectedClass ? characterClasses[selectedClass] : null;
  const selectedRaceData = selectedRace ? characterRaces[selectedRace] : null;

  return (
    <div className="character-selection-ui">
      <div className="character-selection-header">
        <h1>🎭 Karakter Oluştur</h1>
        <p>Fantasy veya Warhammer 40K dünyasında kendi karakterini yarat!</p>
      </div>

      <div className="character-selection-content">
        {/* Sol/Orta Panel - Sınıf Seçimi */}
        <div className="left-panel">
          {/* Filtreler */}
          <div className="filters">
            <div className="filter-group">
              <label>Tema:</label>
              <select
                value={selectedTheme}
                onChange={(e) => setSelectedTheme(e.target.value)}
              >
                <option value="all">Tüm Temalar</option>
                {themes.map(theme => (
                  <option key={theme} value={theme}>
                    {theme === "fantasy" ? "Fantasy" : "Warhammer 40K"}
                  </option>
                ))}
              </select>
            </div>
            <div className="filter-group">
              <label>Rol:</label>
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
              >
                <option value="all">Tüm Roller</option>
                {roles.map(role => (
                  <option key={role} value={role}>
                    {role === "tank" ? "Tank" : 
                     role === "damage_dealer" ? "Hasar" :
                     role === "support" ? "Destek" : "Dengeli"}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Sınıf Seçimi */}
          <div className="class-selection">
            <h3>⚔️ Sınıf Seç</h3>
            <div className="class-grid">
              {filteredClasses.map(([id, charClass]) => (
                <div
                  key={id}
                  className={`class-card ${selectedClass === id ? "selected" : ""}`}
                  onClick={() => setSelectedClass(id)}
                >
                  <div className="class-icon">{getClassIcon(id)}</div>
                  <div className="class-info">
                    <h4>{charClass.name}</h4>
                    <p>{charClass.description}</p>
                    <div className="class-stats">
                      <span>❤️ {charClass.base_hp}</span>
                      <span>⚔️ {charClass.base_attack}</span>
                      <span>🛡️ {charClass.base_defense}</span>
                    </div>
                    <div className="class-tags">
                      <span
                        className="role-tag"
                        style={{ backgroundColor: getRoleColor(charClass.role) }}
                      >
                        {charClass.role === "tank" ? "Tank" : 
                         charClass.role === "damage_dealer" ? "Hasar" :
                         charClass.role === "support" ? "Destek" : "Dengeli"}
                      </span>
                      <span
                        className="theme-tag"
                        style={{ backgroundColor: getThemeColor(charClass.theme) }}
                      >
                        {charClass.theme === "fantasy" ? "Fantasy" : "40K"}
                      </span>
                    </div>
                  </div>
                  <button
                    className="details-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowDetails(showDetails === id ? null : id);
                    }}
                  >
                    📊
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Sınıf Detayları */}
          {showDetails && characterClasses[showDetails] && (
            <div className="class-details">
              <h3>{characterClasses[showDetails].name} Detayları</h3>
              <div className="details-grid">
                <div className="detail-section">
                  <h4>📊 Temel İstatistikler</h4>
                  <div className="stats-grid">
                    <div className="stat-item">
                      <span>Güç:</span>
                      <span>{characterClasses[showDetails].base_stats.strength}</span>
                    </div>
                    <div className="stat-item">
                      <span>Çeviklik:</span>
                      <span>{characterClasses[showDetails].base_stats.dexterity}</span>
                    </div>
                    <div className="stat-item">
                      <span>Dayanıklılık:</span>
                      <span>{characterClasses[showDetails].base_stats.constitution}</span>
                    </div>
                    <div className="stat-item">
                      <span>Zeka:</span>
                      <span>{characterClasses[showDetails].base_stats.intelligence}</span>
                    </div>
                    <div className="stat-item">
                      <span>Bilgelik:</span>
                      <span>{characterClasses[showDetails].base_stats.wisdom}</span>
                    </div>
                    <div className="stat-item">
                      <span>Karizma:</span>
                      <span>{characterClasses[showDetails].base_stats.charisma}</span>
                    </div>
                  </div>
                </div>
                <div className="detail-section">
                  <h4>⚡ Özel Yetenekler</h4>
                  <ul>
                    {characterClasses[showDetails].special_abilities.map((ability, index) => (
                      <li key={index}>{ability}</li>
                    ))}
                  </ul>
                </div>
                <div className="detail-section">
                  <h4>🎒 Başlangıç Ekipmanı</h4>
                  <ul>
                    {characterClasses[showDetails].starting_equipment.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Sağ Panel - Karakter Adı ve Butonlar */}
        <div className="right-panel">
          {/* Karakter Adı */}
          <div className="character-name">
            <h3>📝 Karakter Adı</h3>
            <input
              type="text"
              placeholder="Karakterinizin adını girin..."
              value={characterName}
              onChange={(e) => setCharacterName(e.target.value)}
              maxLength={20}
            />
          </div>

          {/* Karakter Oluştur ve Oyun Başlat Butonları */}
          <div className="character-actions">
            <button
              className="create-character-btn"
              onClick={handleCreateCharacter}
              disabled={!selectedClass || !characterName.trim() || isLoading}
            >
              {isLoading ? "Oluşturuluyor..." : "🎮 Karakteri Oluştur"}
            </button>
            
            <button
              className="start-game-btn"
              onClick={onStartGame}
              disabled={!selectedClass || !characterName.trim()}
            >
              🚀 Oyunu Başlat
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CharacterSelectionUI; 