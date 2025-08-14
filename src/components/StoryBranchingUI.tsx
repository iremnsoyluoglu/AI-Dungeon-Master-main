import React, { useState, useEffect } from 'react';
import './StoryBranchingUI.css';

interface StoryBranchingUIProps {
  storyData: any;
  onChoiceMade: (choiceId: string, diceResult?: number) => void;
  onClose: () => void;
}

interface Choice {
  id: string;
  text: string;
  choice_type: string;
  required_skill?: string;
  required_stat?: string;
  dice_roll?: string;
  difficulty_class?: number;
  consequences: any[];
  next_scene?: string;
  is_available: boolean;
  is_hidden: boolean;
}

interface StoryNode {
  id: string;
  title: string;
  description: string;
  background?: string;
  npcs: string[];
  choices: Choice[];
  is_combat: boolean;
  is_boss_fight: boolean;
  is_ending: boolean;
}

const StoryBranchingUI: React.FC<StoryBranchingUIProps> = ({
  storyData,
  onChoiceMade,
  onClose
}) => {
  const [selectedChoice, setSelectedChoice] = useState<string>('');
  const [diceResult, setDiceResult] = useState<number | null>(null);
  const [isRollingDice, setIsRollingDice] = useState(false);
  const [showConsequences, setShowConsequences] = useState(false);
  const [currentConsequences, setCurrentConsequences] = useState<any>(null);

  const handleChoiceClick = (choice: Choice) => {
    setSelectedChoice(choice.id);
    
    // If choice requires dice roll, show dice interface
    if (choice.dice_roll && choice.difficulty_class) {
      setIsRollingDice(true);
    } else {
      // Make choice immediately
      makeChoice(choice.id);
    }
  };

  const rollDice = async (diceNotation: string) => {
    try {
      const response = await fetch('/api/dice/roll', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dice_notation: diceNotation })
      });
      
      if (response.ok) {
        const result = await response.json();
        return result.total;
      }
    } catch (error) {
      console.error('Error rolling dice:', error);
    }
    
    // Fallback to random roll
    const [numDice, sides] = diceNotation.split('d').map(Number);
    return Math.floor(Math.random() * (sides * numDice)) + numDice;
  };

  const handleDiceRoll = async (choice: Choice) => {
    if (!choice.dice_roll) return;
    
    setIsRollingDice(true);
    
    try {
      const result = await rollDice(choice.dice_roll);
      setDiceResult(result);
      
      // Show dice result briefly
      setTimeout(() => {
        setIsRollingDice(false);
        makeChoice(choice.id, result);
      }, 1500);
      
    } catch (error) {
      console.error('Error rolling dice:', error);
      setIsRollingDice(false);
    }
  };

  const makeChoice = (choiceId: string, diceResult?: number) => {
    setSelectedChoice('');
    setDiceResult(null);
    setIsRollingDice(false);
    
    // Call parent handler
    onChoiceMade(choiceId, diceResult);
  };

  const getChoiceIcon = (choiceType: string): string => {
    const icons: { [key: string]: string } = {
      combat: '⚔️',
      dialogue: '💬',
      exploration: '🗺️',
      stealth: '👤',
      magic: '🔮',
      social: '🤝',
      trade: '💰',
      crafting: '⚒️'
    };
    return icons[choiceType] || '❓';
  };

  const getChoiceColor = (choiceType: string): string => {
    const colors: { [key: string]: string } = {
      combat: '#e74c3c',
      dialogue: '#3498db',
      exploration: '#27ae60',
      stealth: '#95a5a6',
      magic: '#9b59b6',
      social: '#f39c12',
      trade: '#f1c40f',
      crafting: '#e67e22'
    };
    return colors[choiceType] || '#34495e';
  };

  const getDifficultyColor = (difficulty: number): string => {
    if (difficulty <= 10) return '#27ae60';
    if (difficulty <= 15) return '#f39c12';
    return '#e74c3c';
  };

  const getDifficultyText = (difficulty: number): string => {
    if (difficulty <= 10) return 'Kolay';
    if (difficulty <= 15) return 'Orta';
    return 'Zor';
  };

  return (
    <div className="story-branching-overlay">
      <div className="story-branching-modal">
        <div className="story-header">
          <h2>{storyData.title}</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        <div className="story-content">
          {storyData.background && (
            <div className="story-background">
              <img src={storyData.background} alt="Story background" />
            </div>
          )}

          <div className="story-description">
            <p>{storyData.description}</p>
          </div>

          {storyData.npcs && storyData.npcs.length > 0 && (
            <div className="story-npcs">
              <h3>Karakterler:</h3>
              <div className="npc-list">
                {storyData.npcs.map((npc: string, index: number) => (
                  <span key={index} className="npc-tag">
                    👤 {npc}
                  </span>
                ))}
              </div>
            </div>
          )}

          {storyData.is_combat && (
            <div className="combat-warning">
              ⚔️ Savaş Zamanı!
            </div>
          )}

          {storyData.is_boss_fight && (
            <div className="boss-warning">
              👹 Boss Savaşı!
            </div>
          )}

          {storyData.is_ending && (
            <div className="ending-notice">
              🏁 Hikayenin Sonu
            </div>
          )}

          <div className="story-choices">
            <h3>Seçeneklerin:</h3>
            <div className="choices-grid">
              {storyData.choices.map((choice: Choice) => (
                <div
                  key={choice.id}
                  className={`choice-card ${selectedChoice === choice.id ? 'selected' : ''} ${!choice.is_available ? 'disabled' : ''}`}
                  onClick={() => choice.is_available && handleChoiceClick(choice)}
                  style={{ borderLeftColor: getChoiceColor(choice.choice_type) }}
                >
                  <div className="choice-header">
                    <span className="choice-icon">
                      {getChoiceIcon(choice.choice_type)}
                    </span>
                    <span className="choice-text">{choice.text}</span>
                  </div>

                  {choice.required_skill && (
                    <div className="choice-requirement">
                      <span className="requirement-label">Gerekli Beceri:</span>
                      <span className="requirement-value">{choice.required_skill}</span>
                    </div>
                  )}

                  {choice.required_stat && (
                    <div className="choice-requirement">
                      <span className="requirement-label">Gerekli Stat:</span>
                      <span className="requirement-value">{choice.required_stat}</span>
                    </div>
                  )}

                  {choice.dice_roll && choice.difficulty_class && (
                    <div className="choice-dice">
                      <span className="dice-label">Zar Atışı:</span>
                      <span className="dice-notation">{choice.dice_roll}</span>
                      <span 
                        className="difficulty-class"
                        style={{ color: getDifficultyColor(choice.difficulty_class) }}
                      >
                        DC {choice.difficulty_class} ({getDifficultyText(choice.difficulty_class)})
                      </span>
                    </div>
                  )}

                  {choice.is_hidden && (
                    <div className="choice-hidden">
                      🔒 Gizli Seçenek
                    </div>
                  )}

                  {!choice.is_available && (
                    <div className="choice-unavailable">
                      ❌ Kullanılamaz
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {isRollingDice && (
            <div className="dice-rolling-overlay">
              <div className="dice-rolling-modal">
                <h3>🎲 Zar Atılıyor...</h3>
                {diceResult && (
                  <div className="dice-result">
                    <span className="result-number">{diceResult}</span>
                    <span className="result-text">
                      {diceResult >= (storyData.choices.find((c: Choice) => c.id === selectedChoice)?.difficulty_class || 0) 
                        ? '✅ Başarılı!' 
                        : '❌ Başarısız!'}
                    </span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="story-footer">
          <div className="story-progress">
            <span>Hikaye İlerlemesi</span>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '75%' }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StoryBranchingUI; 