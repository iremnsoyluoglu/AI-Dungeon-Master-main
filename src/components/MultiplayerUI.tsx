import React, { useState, useEffect, useRef } from "react";
import "./MultiplayerUI.css";
import { FRPGameUI } from "./FRPGameUI";

interface LobbySession {
  id: string;
  name: string;
  scenario_id: string;
  max_players: number;
  current_players: Player[];
  status: "lobby" | "in_game" | "combat" | "finished";
  created_at: string;
  player_count: number;
}

interface Player {
  id: string;
  username: string;
  status: "online" | "offline" | "afk" | "in_combat";
  joined_at: string;
  character_id?: string;
}

interface ChatMessage {
  id: string;
  player_id: string;
  username: string;
  message: string;
  timestamp: string;
}

interface MultiplayerUIProps {
  onJoinSession: (sessionId: string) => void;
  onLeaveSession: () => void;
  currentSessionId?: string;
}

export const MultiplayerUI: React.FC<MultiplayerUIProps> = ({
  onJoinSession,
  onLeaveSession,
  currentSessionId,
}) => {
  const [lobbySessions, setLobbySessions] = useState<LobbySession[]>([]);
  const [selectedScenario, setSelectedScenario] = useState<string>(
    "scenario_e94fc2090b9194d2"
  );
  const [availableScenarios, setAvailableScenarios] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showCreateSession, setShowCreateSession] = useState(false);
  const [newSessionName, setNewSessionName] = useState("");
  const [maxPlayers, setMaxPlayers] = useState(4);

  // Session state
  const [currentSession, setCurrentSession] = useState<LobbySession | null>(
    null
  );
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [newChatMessage, setNewChatMessage] = useState("");
  const [playerId] = useState(
    `player_${Math.random().toString(36).substr(2, 9)}`
  );
  const [username] = useState(`Player_${Math.floor(Math.random() * 1000)}`);

  // WebSocket connection
  const wsRef = useRef<WebSocket | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadScenarios();
    loadLobbySessions();
    const interval = setInterval(loadLobbySessions, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, [selectedScenario]);

  const loadScenarios = async () => {
    try {
      const response = await fetch("/api/scenarios");
      if (response.ok) {
        const data = await response.json();
        if (data.success && data.scenarios) {
          setAvailableScenarios(data.scenarios);
        } else {
          setAvailableScenarios(data);
        }
      }
    } catch (error) {
      console.error("Error loading scenarios:", error);
    }
  };

  useEffect(() => {
    if (currentSessionId) {
      connectToSession();
    } else {
      disconnectFromSession();
    }
  }, [currentSessionId]);

  useEffect(() => {
    // Auto-scroll chat to bottom
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [chatMessages]);

  const loadLobbySessions = async () => {
    try {
      const response = await fetch(
        `/api/multiplayer/lobby/${selectedScenario}`
      );
      if (response.ok) {
        const sessions = await response.json();
        setLobbySessions(sessions);
      }
    } catch (error) {
      console.error("Error loading lobby sessions:", error);
    }
  };

  const connectToSession = () => {
    if (!currentSessionId) return;

    // Create WebSocket connection
    const ws = new WebSocket(`ws://localhost:8000/ws`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket connected");
      // Send connection message
      ws.send(
        JSON.stringify({
          type: "connect",
          player_id: playerId,
          username: username,
        })
      );

      // Join session
      ws.send(
        JSON.stringify({
          type: "join_session",
          session_id: currentSessionId,
          player_id: playerId,
          username: username,
        })
      );
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleWebSocketMessage(data);
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  };

  const disconnectFromSession = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setCurrentSession(null);
    setChatMessages([]);
  };

  const handleWebSocketMessage = (data: any) => {
    switch (data.type) {
      case "session_update":
        setCurrentSession(data.session);
        break;
      case "chat_message":
        setChatMessages((prev) => [...prev, data.message]);
        break;
      case "player_joined":
        // Handle player joined
        break;
      case "player_left":
        // Handle player left
        break;
      case "error":
        console.error("WebSocket error:", data.error);
        break;
    }
  };

  const createSession = async () => {
    if (!newSessionName.trim()) return;

    setIsLoading(true);
    try {
      const response = await fetch("/api/multiplayer/sessions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: newSessionName,
          scenario_id: selectedScenario,
          max_players: maxPlayers,
          creator_id: playerId,
        }),
      });

      if (response.ok) {
        const session = await response.json();
        onJoinSession(session.id);
        setShowCreateSession(false);
        setNewSessionName("");
      }
    } catch (error) {
      console.error("Error creating session:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const joinSession = async (sessionId: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `/api/multiplayer/sessions/${sessionId}/join`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            player_id: playerId,
            username: username,
          }),
        }
      );

      if (response.ok) {
        onJoinSession(sessionId);
      }
    } catch (error) {
      console.error("Error joining session:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const leaveSession = async () => {
    if (!currentSessionId) return;

    try {
      await fetch(`/api/multiplayer/sessions/${currentSessionId}/leave`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          player_id: playerId,
        }),
      });

      onLeaveSession();
    } catch (error) {
      console.error("Error leaving session:", error);
    }
  };

  const sendChatMessage = () => {
    if (!newChatMessage.trim() || !wsRef.current || !currentSessionId) return;

    wsRef.current.send(
      JSON.stringify({
        type: "chat_message",
        session_id: currentSessionId,
        player_id: playerId,
        message: newChatMessage,
      })
    );

    setNewChatMessage("");
  };

  const startSession = async () => {
    if (!currentSessionId) return;

    try {
      const response = await fetch(
        `/api/multiplayer/sessions/${currentSessionId}/start`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            creator_id: playerId,
          }),
        }
      );

      if (response.ok) {
        // Session started - game will begin
        console.log("Session started!");
      }
    } catch (error) {
      console.error("Error starting session:", error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "online":
        return "#4CAF50";
      case "afk":
        return "#FF9800";
      case "in_combat":
        return "#F44336";
      default:
        return "#9E9E9E";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "online":
        return "🟢";
      case "afk":
        return "🟡";
      case "in_combat":
        return "⚔️";
      default:
        return "⚫";
    }
  };

  if (currentSession) {
    // Check if game has started
    if (currentSession.status === "in_game") {
      return (
        <FRPGameUI
          sessionId={currentSessionId!}
          playerId={playerId}
          onLeaveSession={leaveSession}
        />
      );
    }

    return (
      <div className="multiplayer-session">
        <div className="session-header">
          <h2>🎮 {currentSession.name}</h2>
                     <div className="session-info">
             <span>
               👥 {currentSession.player_count}/{currentSession.max_players}
             </span>
             <span>🏰 {availableScenarios.find(s => s.id === currentSession.scenario_id)?.title || currentSession.scenario_id}</span>
             <span>📊 {currentSession.status}</span>
           </div>
          <button className="leave-btn" onClick={leaveSession}>
            🚪 Leave Session
          </button>
        </div>

        <div className="session-content">
          <div className="players-panel">
            <h3>👥 Players</h3>
            <div className="players-list">
              {currentSession.current_players.map((player) => (
                <div key={player.id} className="player-item">
                  <span
                    className="player-status"
                    style={{ color: getStatusColor(player.status) }}
                  >
                    {getStatusIcon(player.status)}
                  </span>
                  <span className="player-name">{player.username}</span>
                  {player.character_id && (
                    <span className="player-character">🎭</span>
                  )}
                </div>
              ))}
            </div>

            {currentSession.player_count >= 1 && (
              <button className="start-btn" onClick={startSession}>
                🚀 FRP Oyununu Başlat
              </button>
            )}
          </div>

          <div className="chat-panel">
            <h3>💬 Chat</h3>
            <div className="chat-messages" ref={chatContainerRef}>
              {chatMessages.map((message) => (
                <div key={message.id} className="chat-message">
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
                placeholder="Type a message..."
              />
              <button onClick={sendChatMessage}>Send</button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="multiplayer-lobby">
      <div className="lobby-header">
        <h2>🎮 Multiplayer Lobby</h2>
        <div className="scenario-filter">
          <label>Scenario:</label>
          <select
            value={selectedScenario}
            onChange={(e) => setSelectedScenario(e.target.value)}
          >
            {availableScenarios.map((scenario) => (
              <option key={scenario.id} value={scenario.id}>
                {scenario.title}
              </option>
            ))}
          </select>
        </div>
        <button
          className="create-session-btn"
          onClick={() => setShowCreateSession(true)}
        >
          ➕ Create Session
        </button>
      </div>

      {showCreateSession && (
        <div className="create-session-modal">
          <div className="modal-content">
            <h3>Create New Session</h3>
            <div className="form-group">
              <label>Session Name:</label>
              <input
                type="text"
                value={newSessionName}
                onChange={(e) => setNewSessionName(e.target.value)}
                placeholder="Enter session name..."
              />
            </div>
            <div className="form-group">
              <label>Scenario:</label>
              <select
                value={selectedScenario}
                onChange={(e) => setSelectedScenario(e.target.value)}
              >
                {availableScenarios.map((scenario) => (
                  <option key={scenario.id} value={scenario.id}>
                    {scenario.title}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Max Players:</label>
              <select
                value={maxPlayers}
                onChange={(e) => setMaxPlayers(Number(e.target.value))}
              >
                <option value={2}>2 Players</option>
                <option value={3}>3 Players</option>
                <option value={4}>4 Players</option>
                <option value={6}>6 Players</option>
              </select>
            </div>
            <div className="modal-actions">
              <button onClick={createSession} disabled={isLoading}>
                {isLoading ? "Creating..." : "Create Session"}
              </button>
              <button onClick={() => setShowCreateSession(false)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="sessions-list">
        <h3>Available Sessions</h3>
        {lobbySessions.length === 0 ? (
          <div className="no-sessions">
            <p>No active sessions found.</p>
            <p>Create a new session to get started!</p>
          </div>
        ) : (
          <div className="sessions-grid">
            {lobbySessions.map((session) => (
              <div key={session.id} className="session-card">
                <div className="session-header">
                  <h4>{session.name}</h4>
                  <span className="session-status">{session.status}</span>
                </div>
                                 <div className="session-info">
                   <span>
                     👥 {session.player_count}/{session.max_players}
                   </span>
                   <span>🏰 {availableScenarios.find(s => s.id === session.scenario_id)?.title || session.scenario_id}</span>
                   <span>
                     ⏰ {new Date(session.created_at).toLocaleTimeString()}
                   </span>
                 </div>
                <div className="session-players">
                  {session.current_players.map((player) => (
                    <span key={player.id} className="player-chip">
                      {player.username}
                    </span>
                  ))}
                </div>
                <button
                  className="join-btn"
                  onClick={() => joinSession(session.id)}
                  disabled={session.player_count >= session.max_players}
                >
                  {session.player_count >= session.max_players
                    ? "Full"
                    : "Join"}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
