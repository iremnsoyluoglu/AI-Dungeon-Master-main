import React, { useState, useEffect } from "react";
import "./NPCInteractionUI.css";

interface NPCInteractionUIProps {
  npcId: string;
  npcName: string;
  npcPersonality: string;
  relationshipLevel: number;
  onInteraction: (action: string) => void;
  onClose: () => void;
}

const NPCInteractionUI: React.FC<NPCInteractionUIProps> = ({
  npcId,
  npcName,
  npcPersonality,
  relationshipLevel,
  onInteraction,
  onClose,
}) => {
  const [selectedAction, setSelectedAction] = useState<string>("");
  const [interactionResult, setInteractionResult] = useState<any>(null);

  const getRelationshipStatus = (level: number): string => {
    if (level >= 80) return "Çok İyi";
    if (level >= 50) return "İyi";
    if (level >= 20) return "Dostane";
    if (level >= 0) return "Nötr";
    if (level >= -20) return "Şüpheli";
    if (level >= -50) return "Kötü";
    return "Düşman";
  };

  const getRelationshipColor = (level: number): string => {
    if (level >= 80) return "#4CAF50";
    if (level >= 50) return "#8BC34A";
    if (level >= 20) return "#CDDC39";
    if (level >= 0) return "#FFC107";
    if (level >= -20) return "#FF9800";
    if (level >= -50) return "#F44336";
    return "#D32F2F";
  };

  const availableActions = [
    { id: "help", name: "Yardım Et", icon: "🤝", morality: "good" },
    { id: "talk", name: "Konuş", icon: "💬", morality: "neutral" },
    { id: "give_item", name: "Hediye Ver", icon: "🎁", morality: "good" },
    { id: "trade", name: "Ticaret Yap", icon: "💰", morality: "neutral" },
    { id: "threaten", name: "Tehdit Et", icon: "😠", morality: "bad" },
    { id: "attack", name: "Saldır", icon: "⚔️", morality: "bad" },
  ];

  const handleActionClick = (action: string) => {
    setSelectedAction(action);
    onInteraction(action);
  };

  const getPersonalityDescription = (personality: string): string => {
    const descriptions: { [key: string]: string } = {
      friendly: "Dostane ve yardımsever",
      grumpy: "Huysuz ama güvenilir",
      neutral: "Tarafsız ve dengeli",
      hostile: "Düşmanca ve tehlikeli",
      mysterious: "Gizemli ve bilinmez",
      wise: "Bilge ve deneyimli",
      greedy: "Açgözlü ve materyalist",
      honorable: "Onurlu ve güvenilir",
    };
    return descriptions[personality] || "Bilinmeyen kişilik";
  };

  return (
    <div className="npc-interaction-overlay">
      <div className="npc-interaction-modal">
        <div className="npc-interaction-header">
          <h2>{npcName}</h2>
          <button className="close-button" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="npc-info">
          <div className="npc-personality">
            <span className="personality-label">Kişilik:</span>
            <span className="personality-value">
              {getPersonalityDescription(npcPersonality)}
            </span>
          </div>

          <div className="relationship-status">
            <span className="relationship-label">İlişki Durumu:</span>
            <span
              className="relationship-value"
              style={{ color: getRelationshipColor(relationshipLevel) }}
            >
              {getRelationshipStatus(relationshipLevel)} ({relationshipLevel})
            </span>
          </div>
        </div>

        <div className="interaction-actions">
          <h3>Etkileşim Seçenekleri</h3>
          <div className="action-grid">
            {availableActions.map((action) => (
              <button
                key={action.id}
                className={`action-button ${action.morality} ${
                  selectedAction === action.id ? "selected" : ""
                }`}
                onClick={() => handleActionClick(action.id)}
              >
                <span className="action-icon">{action.icon}</span>
                <span className="action-name">{action.name}</span>
              </button>
            ))}
          </div>
        </div>

        {interactionResult && (
          <div className="interaction-result">
            <h3>Etkileşim Sonucu</h3>
            <div className="result-content">
              <p>
                <strong>Eylem:</strong> {interactionResult.action}
              </p>
              <p>
                <strong>İlişki Değişimi:</strong>{" "}
                {interactionResult.relationship_change > 0 ? "+" : ""}
                {interactionResult.relationship_change}
              </p>
              <p>
                <strong>Yeni İlişki Seviyesi:</strong>{" "}
                {interactionResult.new_relationship_level}
              </p>
              <p>
                <strong>NPC Yanıtı:</strong> {interactionResult.response}
              </p>
              {interactionResult.consequences && (
                <div className="consequences">
                  <h4>Sonuçlar:</h4>
                  <ul>
                    {interactionResult.consequences.quest_available && (
                      <li>✅ Quest mevcut</li>
                    )}
                    {interactionResult.consequences.item_offered && (
                      <li>
                        🎁 {interactionResult.consequences.item_offered} sunuldu
                      </li>
                    )}
                    {interactionResult.consequences.combat_assistance && (
                      <li>⚔️ Savaşta yardım edecek</li>
                    )}
                    {interactionResult.consequences.boss_fight_help && (
                      <li>👑 Boss savaşında yardım edecek</li>
                    )}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="moral-info">
          <h3>Moral Durum</h3>
          <div className="moral-stats">
            <div className="moral-stat">
              <span className="stat-label">Genel Hizalama:</span>
              <span className="stat-value">
                {interactionResult?.player_moral?.overall_alignment || "Nötr"}
              </span>
            </div>
            <div className="moral-stat">
              <span className="stat-label">Karma Puanı:</span>
              <span className="stat-value">
                {interactionResult?.player_moral?.karma_points || 0}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NPCInteractionUI;
