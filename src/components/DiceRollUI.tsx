import React, { useState, useEffect } from "react";
import "./DiceRollUI.css";

interface DiceRollProps {
  diceType: string;
  numberOfDice: number;
  modifier: number;
  targetNumber?: number;
  onRoll: (result: DiceRollResult) => void;
  isRolling?: boolean;
}

interface DiceRollResult {
  diceType: string;
  rolls: number[];
  modifier: number;
  total: number;
  targetNumber?: number;
  success?: boolean;
  criticalSuccess?: boolean;
  criticalFailure?: boolean;
}

export const DiceRollUI: React.FC<DiceRollProps> = ({
  diceType,
  numberOfDice,
  modifier,
  targetNumber,
  onRoll,
  isRolling = false,
}) => {
  const [isRollingState, setIsRollingState] = useState(false);
  const [lastResult, setLastResult] = useState<DiceRollResult | null>(null);
  const [rollHistory, setRollHistory] = useState<DiceRollResult[]>([]);

  const rollDice = () => {
    if (isRollingState) return;

    setIsRollingState(true);

    // Simulate dice rolling animation
    setTimeout(() => {
      const rolls: number[] = [];
      const maxValue = parseInt(diceType.replace("d", ""));

      for (let i = 0; i < numberOfDice; i++) {
        rolls.push(Math.floor(Math.random() * maxValue) + 1);
      }

      const total = rolls.reduce((sum, roll) => sum + roll, 0) + modifier;
      const result: DiceRollResult = {
        diceType,
        rolls,
        modifier,
        total,
        targetNumber,
        success: targetNumber ? total >= targetNumber : undefined,
        criticalSuccess: rolls.some((roll) => roll === maxValue),
        criticalFailure: rolls.some((roll) => roll === 1),
      };

      setLastResult(result);
      setRollHistory((prev) => [result, ...prev.slice(0, 4)]); // Keep last 5 rolls
      onRoll(result);
      setIsRollingState(false);
    }, 1000);
  };

  const getDiceIcon = (diceType: string) => {
    switch (diceType) {
      case "d4":
        return "🔶";
      case "d6":
        return "🎲";
      case "d8":
        return "🔷";
      case "d10":
        return "🔸";
      case "d12":
        return "🔹";
      case "d20":
        return "🎯";
      case "d100":
        return "💯";
      default:
        return "🎲";
    }
  };

  const getResultClass = (result: DiceRollResult) => {
    if (result.criticalSuccess) return "critical-success";
    if (result.criticalFailure) return "critical-failure";
    if (result.success) return "success";
    if (result.success === false) return "failure";
    return "";
  };

  return (
    <div className="dice-roll-container">
      <div className="dice-info">
        <span className="dice-icon">{getDiceIcon(diceType)}</span>
        <span className="dice-text">
          {numberOfDice > 1 ? `${numberOfDice}${diceType}` : diceType}
          {modifier > 0 ? ` +${modifier}` : modifier < 0 ? ` ${modifier}` : ""}
        </span>
        {targetNumber && (
          <span className="target-number">Target: {targetNumber}</span>
        )}
      </div>

      <button
        className={`roll-button ${isRollingState ? "rolling" : ""}`}
        onClick={rollDice}
        disabled={isRollingState || isRolling}
      >
        {isRollingState ? "🎲 Rolling..." : "🎲 Roll Dice"}
      </button>

      {lastResult && (
        <div className={`roll-result ${getResultClass(lastResult)}`}>
          <div className="result-header">
            <span className="result-total">{lastResult.total}</span>
            <span className="result-breakdown">
              ({lastResult.rolls.join(" + ")} + {lastResult.modifier})
            </span>
          </div>

          {lastResult.criticalSuccess && (
            <div className="critical-indicator success">
              🎉 Critical Success!
            </div>
          )}
          {lastResult.criticalFailure && (
            <div className="critical-indicator failure">
              💥 Critical Failure!
            </div>
          )}
          {lastResult.success !== undefined &&
            !lastResult.criticalSuccess &&
            !lastResult.criticalFailure && (
              <div
                className={`success-indicator ${
                  lastResult.success ? "success" : "failure"
                }`}
              >
                {lastResult.success ? "✅ Success!" : "❌ Failure!"}
              </div>
            )}
        </div>
      )}

      {rollHistory.length > 0 && (
        <div className="roll-history">
          <h4>Recent Rolls</h4>
          <div className="history-list">
            {rollHistory.map((roll, index) => (
              <div
                key={index}
                className={`history-item ${getResultClass(roll)}`}
              >
                <span className="history-dice">{roll.diceType}</span>
                <span className="history-total">{roll.total}</span>
                <span className="history-breakdown">
                  ({roll.rolls.join("+")}+{roll.modifier})
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Status Effect Display Component
interface StatusEffectDisplayProps {
  effects: Array<{
    id: string;
    name: string;
    type: "buff" | "debuff" | "neutral";
    description: string;
    duration: number;
    icon?: string;
  }>;
}

export const StatusEffectDisplay: React.FC<StatusEffectDisplayProps> = ({
  effects,
}) => {
  const getEffectIcon = (type: string, name: string) => {
    switch (type) {
      case "buff":
        return "⬆️";
      case "debuff":
        return "⬇️";
      case "neutral":
        return "➡️";
      default:
        return "⚡";
    }
  };

  const getEffectClass = (type: string) => {
    switch (type) {
      case "buff":
        return "buff";
      case "debuff":
        return "debuff";
      case "neutral":
        return "neutral";
      default:
        return "";
    }
  };

  return (
    <div className="status-effects-container">
      <h4>Status Effects</h4>
      <div className="effects-list">
        {effects.map((effect) => (
          <div
            key={effect.id}
            className={`effect-item ${getEffectClass(effect.type)}`}
          >
            <span className="effect-icon">
              {getEffectIcon(effect.type, effect.name)}
            </span>
            <span className="effect-name">{effect.name}</span>
            <span className="effect-duration">{effect.duration} rounds</span>
            <span className="effect-description">{effect.description}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
