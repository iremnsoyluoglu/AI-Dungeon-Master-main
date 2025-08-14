import React, { useState, useEffect } from 'react';
import { DiceRollUI } from './DiceRollUI';
import { StatusEffectDisplay } from './DiceRollUI';
import './CombatUI.css';

interface CombatUIProps {
  encounter: {
    id: string;
    title: string;
    description: string;
    enemies: Array<{
      id: string;
      name: string;
      hp: number;
      maxHp: number;
      attack: number;
      defense: number;
      statusEffects: Array<{
        id: string;
        name: string;
        type: 'buff' | 'debuff' | 'neutral';
        description: string;
        duration: number;
      }>;
    }>;
    initiativeOrder: string[];
    currentRound: number;
    currentTurn: number;
  };
  onAction: (action: string, targetId?: string) => void;
}

export const CombatUI: React.FC<CombatUIProps> = ({ encounter, onAction }) => {
  const [selectedAction, setSelectedAction] = useState<string>('');
  const [selectedTarget, setSelectedTarget] = useState<string>('');
  const [isPlayerTurn, setIsPlayerTurn] = useState(true);

  const actions = [
    { id: 'attack', name: '⚔️ Attack', diceType: 'd20', targetRequired: true },
    { id: 'defend', name: '🛡️ Defend', diceType: 'd20', targetRequired: false },
    { id: 'special', name: '✨ Special', diceType: 'd20', targetRequired: true },
    { id: 'item', name: '🧪 Use Item', diceType: 'd6', targetRequired: false },
    { id: 'spell', name: '🔮 Cast Spell', diceType: 'd20', targetRequired: true }
  ];

  const handleAction = (actionId: string) => {
    setSelectedAction(actionId);
    setSelectedTarget('');
  };

  const handleTargetSelect = (targetId: string) => {
    setSelectedTarget(targetId);
  };

  const executeAction = () => {
    if (selectedAction && (!actions.find(a => a.id === selectedAction)?.targetRequired || selectedTarget)) {
      onAction(selectedAction, selectedTarget);
      setSelectedAction('');
      setSelectedTarget('');
    }
  };

  const getInitiativeIcon = (index: number) => {
    if (index === encounter.currentTurn) return '🎯';
    if (index < encounter.currentTurn) return '✅';
    return '⏳';
  };

  const getHpPercentage = (current: number, max: number) => {
    return Math.max(0, Math.min(100, (current / max) * 100));
  };

  const getHpColor = (percentage: number) => {
    if (percentage > 60) return '#4CAF50';
    if (percentage > 30) return '#FF9800';
    return '#F44336';
  };

  return (
    <div className="combat-ui-container">
      <div className="combat-header">
        <h2>⚔️ {encounter.title}</h2>
        <p>{encounter.description}</p>
        <div className="combat-info">
          <span>Round: {encounter.currentRound}</span>
          <span>Turn: {encounter.currentTurn + 1}</span>
        </div>
      </div>

      <div className="initiative-tracker">
        <h3>🎯 Initiative Order</h3>
        <div className="initiative-list">
          {encounter.initiativeOrder.map((characterId, index) => {
            const character = encounter.enemies.find(e => e.id === characterId) || 
                            { name: 'Player', hp: 100, maxHp: 100 };
            return (
              <div 
                key={characterId} 
                className={`initiative-item ${index === encounter.currentTurn ? 'current-turn' : ''}`}
              >
                <span className="initiative-icon">{getInitiativeIcon(index)}</span>
                <span className="character-name">{character.name}</span>
                <div className="hp-bar">
                  <div 
                    className="hp-fill"
                    style={{ 
                      width: `${getHpPercentage(character.hp, character.maxHp)}%`,
                      backgroundColor: getHpColor(getHpPercentage(character.hp, character.maxHp))
                    }}
                  />
                </div>
                <span className="hp-text">{character.hp}/{character.maxHp}</span>
              </div>
            );
          })}
        </div>
      </div>

      <div className="combat-main">
        <div className="enemies-section">
          <h3>👹 Enemies</h3>
          <div className="enemies-grid">
            {encounter.enemies.map(enemy => (
              <div 
                key={enemy.id} 
                className={`enemy-card ${selectedTarget === enemy.id ? 'selected' : ''}`}
                onClick={() => handleTargetSelect(enemy.id)}
              >
                <h4>{enemy.name}</h4>
                <div className="enemy-stats">
                  <div className="stat">
                    <span className="stat-label">HP:</span>
                    <div className="hp-bar">
                      <div 
                        className="hp-fill"
                        style={{ 
                          width: `${getHpPercentage(enemy.hp, enemy.maxHp)}%`,
                          backgroundColor: getHpColor(getHpPercentage(enemy.hp, enemy.maxHp))
                        }}
                      />
                    </div>
                    <span className="stat-value">{enemy.hp}/{enemy.maxHp}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">ATK:</span>
                    <span className="stat-value">{enemy.attack}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">DEF:</span>
                    <span className="stat-value">{enemy.defense}</span>
                  </div>
                </div>
                {enemy.statusEffects.length > 0 && (
                  <div className="enemy-status">
                    {enemy.statusEffects.map(effect => (
                      <span 
                        key={effect.id} 
                        className={`status-badge ${effect.type}`}
                        title={effect.description}
                      >
                        {effect.name} ({effect.duration})
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="player-actions">
          <h3>🎮 Your Actions</h3>
          <div className="action-buttons">
            {actions.map(action => (
              <button
                key={action.id}
                className={`action-btn ${selectedAction === action.id ? 'selected' : ''}`}
                onClick={() => handleAction(action.id)}
              >
                {action.name}
              </button>
            ))}
          </div>

          {selectedAction && (
            <div className="action-details">
              <h4>Selected Action: {actions.find(a => a.id === selectedAction)?.name}</h4>
              
              {actions.find(a => a.id === selectedAction)?.targetRequired && (
                <div className="target-selection">
                  <h5>Select Target:</h5>
                  <div className="target-buttons">
                    {encounter.enemies.map(enemy => (
                      <button
                        key={enemy.id}
                        className={`target-btn ${selectedTarget === enemy.id ? 'selected' : ''}`}
                        onClick={() => handleTargetSelect(enemy.id)}
                      >
                        {enemy.name}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {selectedAction && (!actions.find(a => a.id === selectedAction)?.targetRequired || selectedTarget) && (
                <div className="action-execution">
                  <DiceRollUI
                    diceType={actions.find(a => a.id === selectedAction)?.diceType || 'd20'}
                    numberOfDice={1}
                    modifier={0}
                    onRoll={(result) => {
                      console.log('Dice roll result:', result);
                      executeAction();
                    }}
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="combat-log">
        <h3>📜 Combat Log</h3>
        <div className="log-entries">
          <div className="log-entry">
            <span className="log-time">Round {encounter.currentRound}, Turn {encounter.currentTurn + 1}</span>
            <span className="log-text">Combat started!</span>
          </div>
          <div className="log-entry">
            <span className="log-time">Round {encounter.currentRound}, Turn {encounter.currentTurn + 1}</span>
            <span className="log-text">Player's turn</span>
          </div>
        </div>
      </div>
    </div>
  );
}; 