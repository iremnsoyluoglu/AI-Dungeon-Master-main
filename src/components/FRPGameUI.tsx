import React, { useState, useEffect, useRef } from "react";
import "./FRPGameUI.css";
import io from "socket.io-client";

interface FRPPlayer {
  id: string;
  username: string;
  character_name: string;
  character_class: string;
  hp: number;
  max_hp: number;
  mana: number;
  max_mana: number;
  level: number;
  xp: number;
  is_current_turn: boolean;
  is_alive: boolean;
  status_effects: string[];
}

interface GameAction {
  type: string;
  description: string;
  dice?: string;
  skill?: string;
  // Remove any outcome hints - choices should be mysterious
}

interface GameState {
  session_id: string;
  scenario_id: string;
  current_phase: string;
  current_narrative: string;
  available_actions: GameAction[];
  current_player_turn?: string;
  round_number: number;
  combat_active: boolean;
  enemies: any[];
  environment: any;
  quest_progress: any;
  group_inventory: string[];
}

interface FRPGameUIProps {
  sessionId: string;
  playerId: string;
  onLeaveSession: () => void;
}

export const FRPGameUI: React.FC<FRPGameUIProps> = ({
  sessionId,
  playerId,
  onLeaveSession,
}) => {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [players, setPlayers] = useState<FRPPlayer[]>([]);
  const [selectedAction, setSelectedAction] = useState<GameAction | null>(null);
  const [diceResult, setDiceResult] = useState<number | null>(null);
  const [isMyTurn, setIsMyTurn] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [chatMessages, setChatMessages] = useState<any[]>([]);
  const [newChatMessage, setNewChatMessage] = useState("");
  const [connectionStatus, setConnectionStatus] = useState("connecting");

  const socketRef = useRef<any>(null);
  const narrativeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    connectToGame();
    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, [sessionId]);

  useEffect(() => {
    // Auto-scroll narrative
    if (narrativeRef.current) {
      narrativeRef.current.scrollTop = narrativeRef.current.scrollHeight;
    }
  }, [gameState?.current_narrative]);

  const connectToGame = () => {
    const socket = io("http://localhost:5050");
    socketRef.current = socket;

    socket.on("connect", () => {
      console.log("Connected to FRP game");
      setConnectionStatus("connected");
      
      // Join the game session
      socket.emit("join_frp_session", {
        session_id: sessionId,
        player_id: playerId,
      });
    });

    socket.on("disconnect", () => {
      console.log("Disconnected from FRP game");
      setConnectionStatus("disconnected");
    });

    socket.on("connected", (data) => {
      console.log("Server confirmed connection:", data);
    });

    socket.on("game_state_update", (data) => {
      console.log("Game state update:", data);
      setGameState({
        session_id: data.session_id,
        scenario_id: data.scenario_id || "fantasy_dragon",
        current_phase: "exploration",
        current_narrative: data.narrative,
        available_actions: data.available_actions || [],
        current_player_turn: data.current_player_turn,
        round_number: 1,
        combat_active: false,
        enemies: [],
        environment: {},
        quest_progress: {},
        group_inventory: []
      });
      setPlayers(data.players || []);
    });

    socket.on("action_result", (data) => {
      console.log("Action result:", data);
      handleActionResult(data);
    });

    socket.on("error", (error) => {
      console.error("Socket error:", error);
      setConnectionStatus("error");
    });
  };

  const handleActionResult = (data: any) => {
    setDiceResult(null);
    setSelectedAction(null);

    // Update game state with new narrative and actions
    setGameState((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        current_narrative: data.narrative,
        available_actions: data.available_actions || prev.available_actions
      };
    });

    // Show action result
    if (data.player_action?.success) {
      console.log("Action successful:", data.narrative);
    } else {
      console.log("Action failed:", data.narrative);
    }
  };

  const handleCombatStart = (data: any) => {
    console.log("Combat started:", data);
    // Handle combat initialization
  };

  const executeAction = async () => {
    if (!selectedAction || !gameState || !socketRef.current) return;

    setIsLoading(true);

    try {
      socketRef.current.emit("player_action", {
        session_id: sessionId,
        player_id: playerId,
        action: {
          type: selectedAction.type,
          description: selectedAction.description,
          dice_result: diceResult,
        },
      });
    } catch (error) {
      console.error("Error executing action:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const rollDice = (diceNotation: string) => {
    // Simple dice rolling - in real implementation, this would be more sophisticated
    const [numDice, sides] = diceNotation.split("d").map(Number);
    let total = 0;
    for (let i = 0; i < numDice; i++) {
      total += Math.floor(Math.random() * sides) + 1;
    }
    setDiceResult(total);
    return total;
  };

  const sendChatMessage = () => {
    if (!newChatMessage.trim() || !socketRef.current) return;

    socketRef.current.emit("chat_message", {
      session_id: sessionId,
      player_id: playerId,
      message: newChatMessage,
    });

    setNewChatMessage("");
  };

  const getPlayerStatusColor = (player: FRPPlayer) => {
    if (!player.is_alive) return "#666";
    if (player.is_current_turn) return "#4CAF50";
    return "#2196F3";
  };

  const getHPColor = (hp: number, maxHp: number) => {
    const percentage = (hp / maxHp) * 100;
    if (percentage > 70) return "#4CAF50";
    if (percentage > 30) return "#FF9800";
    return "#F44336";
  };

  if (!gameState) {
    return (
      <div className="frp-loading">
        <div className="loading-spinner"></div>
        <h2>🎮 FRP Oyunu Yükleniyor...</h2>
        <p>AI Dungeon Master hazırlanıyor...</p>
      </div>
    );
  }

  return (
    <div className="frp-game-container">
      {/* Game Header */}
      <div className="frp-header">
        <h1>
          🎲{" "}
          {gameState.scenario_id === "fantasy_dragon"
            ? "🐉 Ejderha Mağarası"
            : "🛡️ Space Marine Görevi"}
        </h1>
        <div className="game-info">
          <span>📊 Tur: {gameState.round_number}</span>
          <span>
            ⚔️ {gameState.combat_active ? "Savaş Modu" : "Keşif Modu"}
          </span>
          <span>👥 {players.length} Oyuncu</span>
        </div>
        <button className="leave-btn" onClick={onLeaveSession}>
          🚪 Oturumdan Ayrıl
        </button>
      </div>

      <div className="frp-content">
        {/* Left Panel - Players & Status */}
        <div className="left-panel">
          <div className="players-section">
            <h3>👥 Oyuncular</h3>
            <div className="players-list">
              {players.map((player) => (
                <div
                  key={player.id}
                  className={`player-card ${
                    player.is_current_turn ? "current-turn" : ""
                  }`}
                  style={{ borderColor: getPlayerStatusColor(player) }}
                >
                  <div className="player-header">
                    <span className="player-name">{player.character_name}</span>
                    <span className="player-class">
                      {player.character_class}
                    </span>
                    {player.is_current_turn && (
                      <span className="turn-indicator">🎯</span>
                    )}
                  </div>

                  <div className="player-stats">
                    <div className="stat-bar">
                      <span>❤️ HP:</span>
                      <div className="progress-bar">
                        <div
                          className="progress-fill"
                          style={{
                            width: `${(player.hp / player.max_hp) * 100}%`,
                            backgroundColor: getHPColor(
                              player.hp,
                              player.max_hp
                            ),
                          }}
                        />
                      </div>
                      <span>
                        {player.hp}/{player.max_hp}
                      </span>
                    </div>

                    <div className="stat-bar">
                      <span>🔮 Mana:</span>
                      <div className="progress-bar">
                        <div
                          className="progress-fill mana-fill"
                          style={{
                            width: `${(player.mana / player.max_mana) * 100}%`,
                          }}
                        />
                      </div>
                      <span>
                        {player.mana}/{player.max_mana}
                      </span>
                    </div>

                    <div className="player-level">
                      <span>
                        📊 Seviye {player.level} (XP: {player.xp})
                      </span>
                    </div>
                  </div>

                  {player.status_effects.length > 0 && (
                    <div className="status-effects">
                      {player.status_effects.map((effect, index) => (
                        <span key={index} className="status-effect">
                          {effect}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Group Inventory */}
          <div className="inventory-section">
            <h3>🎒 Grup Envanteri</h3>
            <div className="inventory-list">
              {gameState.group_inventory.length > 0 ? (
                gameState.group_inventory.map((item, index) => (
                  <span key={index} className="inventory-item">
                    {item}
                  </span>
                ))
              ) : (
                <span className="empty-inventory">Envanter boş</span>
              )}
            </div>
          </div>
        </div>

        {/* Center Panel - Narrative & Actions */}
        <div className="center-panel">
          {/* AI DM Narrative */}
          <div className="narrative-section">
            <h3>🎭 AI Dungeon Master</h3>
            <div className="narrative-content" ref={narrativeRef}>
              {gameState.current_narrative}
            </div>
          </div>

          {/* Available Actions */}
          <div className="actions-section">
            <h3>🎯 Seçenekleriniz</h3>
            <div className="actions-grid">
              {gameState.available_actions.map((action, index) => (
                <button
                  key={index}
                  className={`action-btn mysterious-choice ${
                    selectedAction === action ? "selected" : ""
                  }`}
                  onClick={() => setSelectedAction(action)}
                  disabled={!isMyTurn || isLoading}
                >
                  <span className="action-icon">
                    {getActionIcon(action.type)}
                  </span>
                  <span className="action-text">{action.description}</span>
                  {action.dice && (
                    <span className="dice-info">🎲 {action.dice}</span>
                  )}
                  <span className="mystery-hint">❓ Sonuç belirsiz...</span>
                </button>
              ))}
            </div>
            <div className="choice-warning">
              ⚠️ Seçimlerinizin sonuçları önceden bilinmez. 
              Her seçim yeni bir yol açar ve sonuçları sadece yapıldıktan sonra ortaya çıkar.
            </div>
          </div>

          {/* Dice Rolling */}
          {selectedAction && selectedAction.dice && (
            <div className="dice-section">
              <h3>🎲 Zar Atışı</h3>
              <div className="dice-controls">
                <button
                  className="dice-btn"
                  onClick={() => rollDice(selectedAction.dice!)}
                  disabled={diceResult !== null}
                >
                  {diceResult
                    ? `Zar: ${diceResult}`
                    : `Zar At (${selectedAction.dice})`}
                </button>
                {diceResult && (
                  <button
                    className="reroll-btn"
                    onClick={() => {
                      setDiceResult(null);
                      rollDice(selectedAction.dice!);
                    }}
                  >
                    🔄 Tekrar At
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Execute Action */}
          {selectedAction && (
            <div className="execute-section">
              <button
                className="execute-btn"
                onClick={executeAction}
                disabled={isLoading || (selectedAction.dice && !diceResult)}
              >
                {isLoading ? "🔄 İşleniyor..." : "⚡ Aksiyonu Gerçekleştir"}
              </button>
            </div>
          )}

          {/* Turn Indicator */}
          {!isMyTurn && (
            <div className="turn-indicator">
              <div className="waiting-message">⏳ Sıranızı bekleyin...</div>
            </div>
          )}
        </div>

        {/* Right Panel - Chat & Combat */}
        <div className="right-panel">
          {/* Chat System */}
          <div className="chat-section">
            <h3>💬 Grup Sohbeti</h3>
            <div className="chat-messages">
              {chatMessages.map((message, index) => (
                <div key={index} className="chat-message">
                  <span className="message-time">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </span>
                  <span className="message-username">{message.username}:</span>
                  <span className="message-text">{message.message}</span>
                </div>
              ))}
            </div>
            <div className="chat-input">
              <input
                type="text"
                value={newChatMessage}
                onChange={(e) => setNewChatMessage(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && sendChatMessage()}
                placeholder="Mesajınızı yazın..."
              />
              <button onClick={sendChatMessage}>Gönder</button>
            </div>
          </div>

          {/* Combat Log */}
          {gameState.combat_active && (
            <div className="combat-section">
              <h3>⚔️ Savaş Günlüğü</h3>
              <div className="combat-log">
                {/* Combat log entries would go here */}
                <div className="combat-entry">Savaş başladı!</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const getActionIcon = (actionType: string): string => {
  switch (actionType) {
    case "explore":
      return "🔍";
    case "talk":
      return "💬";
    case "attack":
      return "⚔️";
    case "cast_spell":
      return "🔮";
    case "stealth":
      return "👤";
    case "investigate":
      return "🔎";
    case "persuade":
      return "🤝";
    case "intimidate":
      return "😠";
    default:
      return "🎯";
  }
};
