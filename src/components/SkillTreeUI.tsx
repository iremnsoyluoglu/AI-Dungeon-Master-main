import React, { useState, useEffect } from 'react';
import './SkillTreeUI.css';

interface Skill {
  name: string;
  level_required: number;
  description: string;
  effect: {
    damage?: number;
    defense_bonus?: number;
    heal_amount?: number;
    duration?: number;
    cooldown?: number;
    [key: string]: any;
  };
}

interface SkillTreeUIProps {
  characterId: string;
  characterClass: string;
  onSkillUnlocked?: (skillName: string) => void;
}

const SkillTreeUI: React.FC<SkillTreeUIProps> = ({
  characterId,
  characterClass,
  onSkillUnlocked
}) => {
  const [characterLevel, setCharacterLevel] = useState(1);
  const [characterXp, setCharacterXp] = useState(0);
  const [skillPoints, setSkillPoints] = useState(0);
  const [availableSkills, setAvailableSkills] = useState<Skill[]>([]);
  const [unlockedSkills, setUnlockedSkills] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCharacterData();
  }, [characterId]);

  const loadCharacterData = async () => {
    try {
      setLoading(true);
      
      // Load character level info
      const levelResponse = await fetch(`/api/characters/${characterId}/level`);
      if (levelResponse.ok) {
        const levelData = await levelResponse.json();
        setCharacterLevel(levelData.level);
        setCharacterXp(levelData.xp);
        setSkillPoints(levelData.skill_points);
      }

      // Load character skills
      const skillsResponse = await fetch(`/api/characters/${characterId}/skills`);
      if (skillsResponse.ok) {
        const skillsData = await skillsResponse.json();
        setAvailableSkills(skillsData.available_skills);
        setUnlockedSkills(skillsData.unlocked_skills);
      }
    } catch (err) {
      setError('Karakter verileri yüklenirken hata oluştu');
      console.error('Error loading character data:', err);
    } finally {
      setLoading(false);
    }
  };

  const unlockSkill = async (skillName: string) => {
    try {
      const response = await fetch(`/api/characters/${characterId}/unlock_skill`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ skill_name: skillName }),
      });

      if (response.ok) {
        const result = await response.json();
        setSkillPoints(result.remaining_skill_points);
        setUnlockedSkills(prev => [...prev, skillName]);
        onSkillUnlocked?.(skillName);
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Skill açılırken hata oluştu');
      }
    } catch (err) {
      setError('Skill açılırken hata oluştu');
      console.error('Error unlocking skill:', err);
    }
  };

  const getSkillCategory = (skill: Skill) => {
    if (skill.level_required <= 2) return 'basic';
    if (skill.level_required <= 4) return 'intermediate';
    return 'ultimate';
  };

  const getSkillCategoryColor = (category: string) => {
    switch (category) {
      case 'basic': return '#4CAF50';
      case 'intermediate': return '#FF9800';
      case 'ultimate': return '#F44336';
      default: return '#757575';
    }
  };

  const canUnlockSkill = (skill: Skill) => {
    return characterLevel >= skill.level_required && 
           skillPoints > 0 && 
           !unlockedSkills.includes(skill.name);
  };

  if (loading) {
    return (
      <div className="skill-tree-container">
        <div className="loading">Yükleniyor...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="skill-tree-container">
        <div className="error">{error}</div>
        <button onClick={loadCharacterData}>Tekrar Dene</button>
      </div>
    );
  }

  return (
    <div className="skill-tree-container">
      <div className="skill-tree-header">
        <h2>🎯 Yetenek Ağacı</h2>
        <div className="character-info">
          <div className="level-info">
            <span className="level">Seviye {characterLevel}</span>
            <div className="xp-bar">
              <div 
                className="xp-fill" 
                style={{ width: `${(characterXp % 100)}%` }}
              ></div>
            </div>
            <span className="xp-text">{characterXp} XP</span>
          </div>
          <div className="skill-points">
            <span className="points">{skillPoints}</span>
            <span className="label">Yetenek Puanı</span>
          </div>
        </div>
      </div>

      <div className="skill-categories">
        <div className="skill-category">
          <h3 style={{ color: getSkillCategoryColor('basic') }}>
            🔰 Temel Yetenekler (Seviye 2+)
          </h3>
          <div className="skills-grid">
            {availableSkills
              .filter(skill => getSkillCategory(skill) === 'basic')
              .map(skill => (
                <div 
                  key={skill.name} 
                  className={`skill-card ${unlockedSkills.includes(skill.name) ? 'unlocked' : ''}`}
                >
                  <div className="skill-header">
                    <h4>{skill.name}</h4>
                    <span className="level-requirement">Seviye {skill.level_required}</span>
                  </div>
                  <p className="skill-description">{skill.description}</p>
                  <div className="skill-effects">
                    {Object.entries(skill.effect).map(([key, value]) => (
                      <span key={key} className="effect">
                        {key}: {value}
                      </span>
                    ))}
                  </div>
                  {canUnlockSkill(skill) && (
                    <button 
                      className="unlock-button"
                      onClick={() => unlockSkill(skill.name)}
                    >
                      Yetenek Aç ({skillPoints} puan)
                    </button>
                  )}
                  {unlockedSkills.includes(skill.name) && (
                    <div className="unlocked-badge">✓ Açıldı</div>
                  )}
                </div>
              ))}
          </div>
        </div>

        <div className="skill-category">
          <h3 style={{ color: getSkillCategoryColor('intermediate') }}>
            ⚔️ Orta Yetenekler (Seviye 4+)
          </h3>
          <div className="skills-grid">
            {availableSkills
              .filter(skill => getSkillCategory(skill) === 'intermediate')
              .map(skill => (
                <div 
                  key={skill.name} 
                  className={`skill-card ${unlockedSkills.includes(skill.name) ? 'unlocked' : ''}`}
                >
                  <div className="skill-header">
                    <h4>{skill.name}</h4>
                    <span className="level-requirement">Seviye {skill.level_required}</span>
                  </div>
                  <p className="skill-description">{skill.description}</p>
                  <div className="skill-effects">
                    {Object.entries(skill.effect).map(([key, value]) => (
                      <span key={key} className="effect">
                        {key}: {value}
                      </span>
                    ))}
                  </div>
                  {canUnlockSkill(skill) && (
                    <button 
                      className="unlock-button"
                      onClick={() => unlockSkill(skill.name)}
                    >
                      Yetenek Aç ({skillPoints} puan)
                    </button>
                  )}
                  {unlockedSkills.includes(skill.name) && (
                    <div className="unlocked-badge">✓ Açıldı</div>
                  )}
                </div>
              ))}
          </div>
        </div>

        <div className="skill-category">
          <h3 style={{ color: getSkillCategoryColor('ultimate') }}>
            🌟 Nihai Yetenekler (Seviye 5+)
          </h3>
          <div className="skills-grid">
            {availableSkills
              .filter(skill => getSkillCategory(skill) === 'ultimate')
              .map(skill => (
                <div 
                  key={skill.name} 
                  className={`skill-card ${unlockedSkills.includes(skill.name) ? 'unlocked' : ''}`}
                >
                  <div className="skill-header">
                    <h4>{skill.name}</h4>
                    <span className="level-requirement">Seviye {skill.level_required}</span>
                  </div>
                  <p className="skill-description">{skill.description}</p>
                  <div className="skill-effects">
                    {Object.entries(skill.effect).map(([key, value]) => (
                      <span key={key} className="effect">
                        {key}: {value}
                      </span>
                    ))}
                  </div>
                  {canUnlockSkill(skill) && (
                    <button 
                      className="unlock-button"
                      onClick={() => unlockSkill(skill.name)}
                    >
                      Yetenek Aç ({skillPoints} puan)
                    </button>
                  )}
                  {unlockedSkills.includes(skill.name) && (
                    <div className="unlocked-badge">✓ Açıldı</div>
                  )}
                </div>
              ))}
          </div>
        </div>
      </div>

      {availableSkills.length === 0 && (
        <div className="no-skills">
          <p>Bu seviyede henüz yetenek bulunmuyor.</p>
          <p>Seviye atlamak için daha fazla XP kazanın!</p>
        </div>
      )}
    </div>
  );
};

export default SkillTreeUI;
