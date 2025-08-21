import React, { useState, useEffect } from "react";
import "./CharacterCreationUI.css";

interface CharacterAttributes {
  strength: number;
  dexterity: number;
  constitution: number;
  intelligence: number;
  wisdom: number;
  charisma: number;
}

interface RaceModifiers {
  strength: number;
  dexterity: number;
  constitution: number;
  intelligence: number;
  wisdom: number;
  charisma: number;
}

interface ClassModifiers {
  strength: number;
  dexterity: number;
  constitution: number;
  intelligence: number;
  wisdom: number;
  charisma: number;
}

interface CharacterCreationUIProps {
  onCharacterCreated: (character: any) => void;
  onBack: () => void;
}

export const CharacterCreationUI: React.FC<CharacterCreationUIProps> = ({
  onCharacterCreated,
  onBack,
}) => {
  const [characterName, setCharacterName] = useState("");
  const [selectedRace, setSelectedRace] = useState("");
  const [selectedClass, setSelectedClass] = useState("");
  const [baseAttributes, setBaseAttributes] = useState<CharacterAttributes>({
    strength: 15,
    dexterity: 12,
    constitution: 16,
    intelligence: 14,
    wisdom: 13,
    charisma: 10,
  });
  const [finalAttributes, setFinalAttributes] = useState<CharacterAttributes>({
    strength: 15,
    dexterity: 12,
    constitution: 16,
    intelligence: 14,
    wisdom: 13,
    charisma: 10,
  });

  // Race definitions with modifiers
  const races = {
    elf: {
      name: "Elf",
      description: "Zarif ve uzun ömürlü, büyüye yatkın",
      icon: "🧝",
      modifiers: {
        strength: 0,
        dexterity: 2,
        constitution: -1,
        intelligence: 1,
        wisdom: 0,
        charisma: 0,
      } as RaceModifiers,
    },
    human: {
      name: "İnsan",
      description: "Dengeli ve uyumlu, her şeye yatkın",
      icon: "👤",
      modifiers: {
        strength: 1,
        dexterity: 1,
        constitution: 1,
        intelligence: 1,
        wisdom: 1,
        charisma: 1,
      } as RaceModifiers,
    },
    dwarf: {
      name: "Cüce",
      description: "Güçlü ve dayanıklı, zanaatkarlıkta usta",
      icon: "🧙",
      modifiers: {
        strength: 1,
        dexterity: -1,
        constitution: 2,
        intelligence: 0,
        wisdom: 0,
        charisma: 0,
      } as RaceModifiers,
    },
    orc: {
      name: "Ork",
      description: "Güçlü ve savaşçı, vahşi doğaya sahip",
      icon: "👹",
      modifiers: {
        strength: 3,
        dexterity: 0,
        constitution: 1,
        intelligence: -2,
        wisdom: 0,
        charisma: -1,
      } as RaceModifiers,
    },
  };

  // Class definitions with modifiers and skills
  const classes = {
    warrior: {
      name: "Savaşçı",
      description: "Güçlü savaşçı, yüksek savunma ve HP",
      icon: "⚔️",
      modifiers: {
        strength: 3,
        dexterity: 0,
        constitution: 2,
        intelligence: -1,
        wisdom: 0,
        charisma: 0,
      } as ClassModifiers,
      skills: [
        {
          id: "heavy_strike",
          name: "Ağır Vuruş",
          description: "Güçlü tek vuruş, yüksek hasar",
          level: 1,
          damage: 25,
          type: "physical",
          icon: "🗡️",
        },
        {
          id: "shield_bash",
          name: "Kalkan Darbesi",
          description: "Kalkanla düşmanı sersemlet",
          level: 3,
          damage: 15,
          type: "stun",
          icon: "🛡️",
        },
        {
          id: "battle_rage",
          name: "Savaş Öfkesi",
          description: "Geçici güç artışı",
          level: 5,
          damage: 0,
          type: "buff",
          icon: "😤",
        },
        {
          id: "whirlwind",
          name: "Kasırga",
          description: "Çevredeki tüm düşmanlara saldır",
          level: 7,
          damage: 20,
          type: "aoe",
          icon: "🌪️",
        },
        {
          id: "berserker",
          name: "Berserker",
          description: "Ultimate skill - maksimum hasar",
          level: 10,
          damage: 50,
          type: "ultimate",
          icon: "⚡",
        },
      ],
    },
    mage: {
      name: "Büyücü",
      description: "Güçlü büyücü, yüksek saldırı ve mana",
      icon: "🔮",
      modifiers: {
        strength: -2,
        dexterity: 0,
        constitution: -1,
        intelligence: 3,
        wisdom: 1,
        charisma: 0,
      } as ClassModifiers,
      skills: [
        {
          id: "fireball",
          name: "Ateş Topu",
          description: "Güçlü ateş büyüsü",
          level: 1,
          damage: 30,
          type: "magic",
          icon: "🔥",
        },
        {
          id: "ice_shard",
          name: "Buz Parçası",
          description: "Düşmanı yavaşlat",
          level: 3,
          damage: 20,
          type: "ice",
          icon: "❄️",
        },
        {
          id: "lightning_bolt",
          name: "Şimşek",
          description: "Anında hasar",
          level: 5,
          damage: 35,
          type: "lightning",
          icon: "⚡",
        },
        {
          id: "meteor_storm",
          name: "Meteor Fırtınası",
          description: "Çoklu hedef hasar",
          level: 7,
          damage: 40,
          type: "aoe",
          icon: "☄️",
        },
        {
          id: "time_stop",
          name: "Zaman Durdurma",
          description: "Ultimate skill - zamanı dondur",
          level: 10,
          damage: 60,
          type: "ultimate",
          icon: "⏰",
        },
      ],
    },
    rogue: {
      name: "Hırsız",
      description: "Hızlı ve gizli, yüksek saldırı ve stealth",
      icon: "🗡️",
      modifiers: {
        strength: 0,
        dexterity: 3,
        constitution: -1,
        intelligence: 1,
        wisdom: 0,
        charisma: 0,
      } as ClassModifiers,
      skills: [
        {
          id: "backstab",
          name: "Sırt Bıçağı",
          description: "Gizli saldırı, kritik hasar",
          level: 1,
          damage: 35,
          type: "stealth",
          icon: "🗡️",
        },
        {
          id: "poison_dart",
          name: "Zehirli Ok",
          description: "Zehir hasarı",
          level: 3,
          damage: 15,
          type: "poison",
          icon: "☠️",
        },
        {
          id: "shadow_step",
          name: "Gölge Adımı",
          description: "Anında hareket",
          level: 5,
          damage: 0,
          type: "movement",
          icon: "👻",
        },
        {
          id: "death_blow",
          name: "Ölüm Vuruşu",
          description: "Yüksek kritik hasar",
          level: 7,
          damage: 45,
          type: "critical",
          icon: "💀",
        },
        {
          id: "assassinate",
          name: "Suikast",
          description: "Ultimate skill - tek vuruş öldür",
          level: 10,
          damage: 100,
          type: "ultimate",
          icon: "⚰️",
        },
      ],
    },
    priest: {
      name: "Rahip",
      description: "İyileştirici, yüksek heal ve savunma",
      icon: "⛪",
      modifiers: {
        strength: -2,
        dexterity: 0,
        constitution: 1,
        intelligence: 0,
        wisdom: 2,
        charisma: 2,
      } as ClassModifiers,
      skills: [
        {
          id: "heal",
          name: "İyileştirme",
          description: "HP geri yükle",
          level: 1,
          damage: -30,
          type: "heal",
          icon: "💚",
        },
        {
          id: "smite",
          name: "Kutsal Vuruş",
          description: "Kutsal hasar",
          level: 3,
          damage: 25,
          type: "holy",
          icon: "✨",
        },
        {
          id: "divine_shield",
          name: "Kutsal Kalkan",
          description: "Savunma artışı",
          level: 5,
          damage: 0,
          type: "shield",
          icon: "🛡️",
        },
        {
          id: "resurrection",
          name: "Diriliş",
          description: "Ölüyü canlandır",
          level: 7,
          damage: 0,
          type: "revive",
          icon: "🕊️",
        },
        {
          id: "divine_wrath",
          name: "Kutsal Öfke",
          description: "Ultimate skill - kutsal fırtına",
          level: 10,
          damage: 70,
          type: "ultimate",
          icon: "⚜️",
        },
      ],
    },
  };

  // Calculate final attributes when race or class changes
  useEffect(() => {
    if (selectedRace && selectedClass) {
      const raceModifiers = races[selectedRace as keyof typeof races].modifiers;
      const classModifiers =
        classes[selectedClass as keyof typeof classes].modifiers;

      const final = {
        strength: Math.max(
          1,
          baseAttributes.strength +
            raceModifiers.strength +
            classModifiers.strength
        ),
        dexterity: Math.max(
          1,
          baseAttributes.dexterity +
            raceModifiers.dexterity +
            classModifiers.dexterity
        ),
        constitution: Math.max(
          1,
          baseAttributes.constitution +
            raceModifiers.constitution +
            classModifiers.constitution
        ),
        intelligence: Math.max(
          1,
          baseAttributes.intelligence +
            raceModifiers.intelligence +
            classModifiers.intelligence
        ),
        wisdom: Math.max(
          1,
          baseAttributes.wisdom + raceModifiers.wisdom + classModifiers.wisdom
        ),
        charisma: Math.max(
          1,
          baseAttributes.charisma +
            raceModifiers.charisma +
            classModifiers.charisma
        ),
      };

      setFinalAttributes(final);
    }
  }, [selectedRace, selectedClass, baseAttributes]);

  const handleAttributeChange = (
    attribute: keyof CharacterAttributes,
    value: number
  ) => {
    setBaseAttributes((prev) => ({
      ...prev,
      [attribute]: Math.max(1, Math.min(20, value)),
    }));
  };

  const getAttributeModifier = (value: number): string => {
    const modifier = Math.floor((value - 10) / 2);
    return modifier >= 0 ? `+${modifier}` : `${modifier}`;
  };

  const getAttributeColor = (value: number): string => {
    if (value >= 18) return "#ff6b6b"; // Red for high
    if (value >= 16) return "#ffa500"; // Orange for good
    if (value >= 14) return "#ffff00"; // Yellow for average
    if (value >= 12) return "#90ee90"; // Light green for below average
    return "#ff69b4"; // Pink for low
  };

  const handleCreateCharacter = () => {
    if (!characterName || !selectedRace || !selectedClass) {
      alert("Lütfen karakter adı, ırk ve sınıf seçin!");
      return;
    }

    const selectedClassData = classes[selectedClass as keyof typeof classes];
    const availableSkills = selectedClassData.skills.filter(
      (skill) => skill.level <= 1
    );

    const character = {
      name: characterName,
      race: selectedRace,
      class: selectedClass,
      baseAttributes,
      finalAttributes,
      level: 1,
      experience: 0,
      hp: 10 + Math.floor((finalAttributes.constitution - 10) / 2),
      maxHp: 10 + Math.floor((finalAttributes.constitution - 10) / 2),
      mana:
        selectedClass === "mage"
          ? 20 + Math.floor((finalAttributes.intelligence - 10) / 2)
          : 0,
      maxMana:
        selectedClass === "mage"
          ? 20 + Math.floor((finalAttributes.intelligence - 10) / 2)
          : 0,
      skills: availableSkills,
      availableSkills: selectedClassData.skills,
      created_at: new Date().toISOString(),
    };

    onCharacterCreated(character);
  };

  const getRaceModifiers = () => {
    if (!selectedRace) return null;
    return races[selectedRace as keyof typeof races].modifiers;
  };

  const getClassModifiers = () => {
    if (!selectedClass) return null;
    return classes[selectedClass as keyof typeof classes].modifiers;
  };

  return (
    <div className="character-creation-ui">
      <div className="creation-header">
        <div className="header-left">
          <button className="back-button" onClick={onBack}>
            ← Geri
          </button>
        </div>
        <div className="header-center">
          <h2>🎭 Karakter Oluştur</h2>
          <p>Dinamik ırk ve sınıf tabanlı attribute sistemi</p>
        </div>
      </div>

      <div className="creation-content">
        {/* Basic Information */}
        <div className="basic-info-section">
          <h3>📝 Temel Bilgiler</h3>
          <div className="input-group">
            <label>Karakter Adı:</label>
            <input
              type="text"
              value={characterName}
              onChange={(e) => setCharacterName(e.target.value)}
              placeholder="Karakterinizin adını girin..."
              className="name-input"
            />
          </div>
        </div>

        {/* Race Selection */}
        <div className="race-selection-section">
          <h3>🧬 Irk Seçimi</h3>
          <div className="race-grid">
            {Object.entries(races).map(([raceKey, race]) => (
              <div
                key={raceKey}
                className={`race-card ${
                  selectedRace === raceKey ? "selected" : ""
                }`}
                onClick={() => setSelectedRace(raceKey)}
              >
                <div className="race-icon">{race.icon}</div>
                <h4>{race.name}</h4>
                <p>{race.description}</p>
                <div className="race-modifiers">
                  <small>Modifiers:</small>
                  {Object.entries(race.modifiers).map(([attr, mod]) => (
                    <span
                      key={attr}
                      className={`modifier ${
                        mod > 0 ? "positive" : mod < 0 ? "negative" : "neutral"
                      }`}
                    >
                      {attr.slice(0, 3).toUpperCase()}: {mod > 0 ? "+" : ""}
                      {mod}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Class Selection */}
        <div className="class-selection-section">
          <h3>⚔️ Sınıf Seçimi</h3>
          <div className="class-grid">
            {Object.entries(classes).map(([classKey, classData]) => (
              <div
                key={classKey}
                className={`class-card ${
                  selectedClass === classKey ? "selected" : ""
                }`}
                onClick={() => setSelectedClass(classKey)}
              >
                <div className="class-icon">{classData.icon}</div>
                <h4>{classData.name}</h4>
                <p>{classData.description}</p>
                <div className="class-modifiers">
                  <small>Modifiers:</small>
                  {Object.entries(classData.modifiers).map(([attr, mod]) => (
                    <span
                      key={attr}
                      className={`modifier ${
                        mod > 0 ? "positive" : mod < 0 ? "negative" : "neutral"
                      }`}
                    >
                      {attr.slice(0, 3).toUpperCase()}: {mod > 0 ? "+" : ""}
                      {mod}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Dynamic Attributes Display */}
        <div className="attributes-section">
          <h3>📊 Dinamik Attribute Hesaplama</h3>
          <div className="attributes-grid">
            {Object.entries(baseAttributes).map(([attrKey, baseValue]) => {
              const attr = attrKey as keyof CharacterAttributes;
              const raceMod = getRaceModifiers()?.[attr] || 0;
              const classMod = getClassModifiers()?.[attr] || 0;
              const finalValue = finalAttributes[attr];

              return (
                <div key={attrKey} className="attribute-card">
                  <div className="attribute-header">
                    <h4>
                      {attrKey.charAt(0).toUpperCase() + attrKey.slice(1)}
                    </h4>
                    <div
                      className="attribute-value"
                      style={{ color: getAttributeColor(finalValue) }}
                    >
                      {finalValue} ({getAttributeModifier(finalValue)})
                    </div>
                  </div>

                  <div className="attribute-breakdown">
                    <div className="breakdown-item">
                      <span>Base:</span>
                      <input
                        type="number"
                        value={baseValue}
                        onChange={(e) =>
                          handleAttributeChange(
                            attr,
                            parseInt(e.target.value) || 1
                          )
                        }
                        min="1"
                        max="20"
                        className="attribute-input"
                      />
                    </div>

                    {selectedRace && (
                      <div className="breakdown-item">
                        <span>Race:</span>
                        <span
                          className={`modifier-display ${
                            raceMod > 0
                              ? "positive"
                              : raceMod < 0
                              ? "negative"
                              : "neutral"
                          }`}
                        >
                          {raceMod > 0 ? "+" : ""}
                          {raceMod}
                        </span>
                      </div>
                    )}

                    {selectedClass && (
                      <div className="breakdown-item">
                        <span>Class:</span>
                        <span
                          className={`modifier-display ${
                            classMod > 0
                              ? "positive"
                              : classMod < 0
                              ? "negative"
                              : "neutral"
                          }`}
                        >
                          {classMod > 0 ? "+" : ""}
                          {classMod}
                        </span>
                      </div>
                    )}

                    <div className="breakdown-item total">
                      <span>Total:</span>
                      <span
                        className="total-value"
                        style={{ color: getAttributeColor(finalValue) }}
                      >
                        {finalValue}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Character Summary */}
        {selectedRace && selectedClass && (
          <div className="character-summary">
            <h3>🎯 Karakter Özeti</h3>
            <div className="summary-content">
              <div className="summary-item">
                <strong>Ad:</strong> {characterName || "Belirtilmemiş"}
              </div>
              <div className="summary-item">
                <strong>Irk:</strong>{" "}
                {races[selectedRace as keyof typeof races].name}{" "}
                {races[selectedRace as keyof typeof races].icon}
              </div>
              <div className="summary-item">
                <strong>Sınıf:</strong>{" "}
                {classes[selectedClass as keyof typeof classes].name}{" "}
                {classes[selectedClass as keyof typeof classes].icon}
              </div>
              <div className="summary-item">
                <strong>HP:</strong>{" "}
                {10 + Math.floor((finalAttributes.constitution - 10) / 2)}
              </div>
              {selectedClass === "mage" && (
                <div className="summary-item">
                  <strong>Mana:</strong>{" "}
                  {20 + Math.floor((finalAttributes.intelligence - 10) / 2)}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Create Button */}
        <div className="create-section">
          <button
            className="create-character-button"
            onClick={handleCreateCharacter}
            disabled={!characterName || !selectedRace || !selectedClass}
          >
            🎭 Karakteri Oluştur
          </button>
        </div>
      </div>
    </div>
  );
};
