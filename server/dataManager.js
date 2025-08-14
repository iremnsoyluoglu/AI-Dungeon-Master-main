const fs = require('fs');
const path = require('path');

class DataManager {
  constructor() {
    this.dataDir = path.join(__dirname, '../data');
    this.ensureDataDirectory();
  }

  ensureDataDirectory() {
    if (!fs.existsSync(this.dataDir)) {
      fs.mkdirSync(this.dataDir, { recursive: true });
    }
  }

  // Oyuncu kayıtları
  getPlayerSaves(playerId) {
    const savesFile = path.join(this.dataDir, 'saves', `${playerId}_saves.json`);
    if (fs.existsSync(savesFile)) {
      return JSON.parse(fs.readFileSync(savesFile, 'utf8'));
    }
    return [];
  }

  savePlayerGame(playerId, saveData) {
    const savesDir = path.join(this.dataDir, 'saves');
    if (!fs.existsSync(savesDir)) {
      fs.mkdirSync(savesDir, { recursive: true });
    }
    
    const savesFile = path.join(savesDir, `${playerId}_saves.json`);
    const saves = this.getPlayerSaves(playerId);
    saves.push(saveData);
    
    fs.writeFileSync(savesFile, JSON.stringify(saves, null, 2));
    return true;
  }

  // Oyuncu karakterleri
  getPlayerCharacters(playerId) {
    const charsFile = path.join(this.dataDir, 'characters', `${playerId}_characters.json`);
    if (fs.existsSync(charsFile)) {
      return JSON.parse(fs.readFileSync(charsFile, 'utf8'));
    }
    return [];
  }

  savePlayerCharacter(playerId, characterData) {
    const charsDir = path.join(this.dataDir, 'characters');
    if (!fs.existsSync(charsDir)) {
      fs.mkdirSync(charsDir, { recursive: true });
    }
    
    const charsFile = path.join(charsDir, `${playerId}_characters.json`);
    const characters = this.getPlayerCharacters(playerId);
    characters.push(characterData);
    
    fs.writeFileSync(charsFile, JSON.stringify(characters, null, 2));
    return true;
  }

  // Oyuncu ilerlemesi
  getPlayerProgress(playerId) {
    const progressFile = path.join(this.dataDir, 'progress', `${playerId}_progress.json`);
    if (fs.existsSync(progressFile)) {
      return JSON.parse(fs.readFileSync(progressFile, 'utf8'));
    }
    return {
      playerId: playerId,
      level: 1,
      experience: 0,
      completedScenarios: [],
      achievements: [],
      lastPlayed: new Date().toISOString()
    };
  }

  updatePlayerProgress(playerId, progressData) {
    const progressDir = path.join(this.dataDir, 'progress');
    if (!fs.existsSync(progressDir)) {
      fs.mkdirSync(progressDir, { recursive: true });
    }
    
    const progressFile = path.join(progressDir, `${playerId}_progress.json`);
    const progress = this.getPlayerProgress(playerId);
    const updatedProgress = { ...progress, ...progressData };
    
    fs.writeFileSync(progressFile, JSON.stringify(updatedProgress, null, 2));
    return true;
  }

  // Senaryo verileri
  getScenarios() {
    const scenariosFile = path.join(this.dataDir, 'scenarios.json');
    if (fs.existsSync(scenariosFile)) {
      return JSON.parse(fs.readFileSync(scenariosFile, 'utf8'));
    }
    return [];
  }

  saveScenario(scenarioData) {
    const scenarios = this.getScenarios();
    scenarios.push(scenarioData);
    
    const scenariosFile = path.join(this.dataDir, 'scenarios.json');
    fs.writeFileSync(scenariosFile, JSON.stringify(scenarios, null, 2));
    return true;
  }

  // NPC verileri
  getNPCs() {
    const npcsFile = path.join(this.dataDir, 'npcs.json');
    if (fs.existsSync(npcsFile)) {
      return JSON.parse(fs.readFileSync(npcsFile, 'utf8'));
    }
    return [];
  }

  saveNPC(npcData) {
    const npcs = this.getNPCs();
    npcs.push(npcData);
    
    const npcsFile = path.join(this.dataDir, 'npcs.json');
    fs.writeFileSync(npcsFile, JSON.stringify(npcs, null, 2));
    return true;
  }

  // Savaş oturumları
  getCombatSessions() {
    const combatFile = path.join(this.dataDir, 'combat_sessions.json');
    if (fs.existsSync(combatFile)) {
      return JSON.parse(fs.readFileSync(combatFile, 'utf8'));
    }
    return [];
  }

  saveCombatSession(sessionData) {
    const sessions = this.getCombatSessions();
    sessions.push(sessionData);
    
    const combatFile = path.join(this.dataDir, 'combat_sessions.json');
    fs.writeFileSync(combatFile, JSON.stringify(sessions, null, 2));
    return true;
  }

  // Kullanıcı verileri
  getUsers() {
    const usersFile = path.join(this.dataDir, 'users.json');
    if (fs.existsSync(usersFile)) {
      return JSON.parse(fs.readFileSync(usersFile, 'utf8'));
    }
    return [];
  }

  saveUser(userData) {
    const users = this.getUsers();
    const existingUserIndex = users.findIndex(u => u.id === userData.id);
    
    if (existingUserIndex >= 0) {
      users[existingUserIndex] = { ...users[existingUserIndex], ...userData };
    } else {
      users.push(userData);
    }
    
    const usersFile = path.join(this.dataDir, 'users.json');
    fs.writeFileSync(usersFile, JSON.stringify(users, null, 2));
    return true;
  }

  // Karma sistemi
  getKarmaData(playerId) {
    const karmaFile = path.join(this.dataDir, 'karma', `${playerId}_karma.json`);
    if (fs.existsSync(karmaFile)) {
      return JSON.parse(fs.readFileSync(karmaFile, 'utf8'));
    }
    return {
      playerId: playerId,
      karma: 0,
      goodActions: 0,
      evilActions: 0,
      neutralActions: 0,
      reputation: {}
    };
  }

  updateKarma(playerId, karmaData) {
    const karmaDir = path.join(this.dataDir, 'karma');
    if (!fs.existsSync(karmaDir)) {
      fs.mkdirSync(karmaDir, { recursive: true });
    }
    
    const karmaFile = path.join(karmaDir, `${playerId}_karma.json`);
    const karma = this.getKarmaData(playerId);
    const updatedKarma = { ...karma, ...karmaData };
    
    fs.writeFileSync(karmaFile, JSON.stringify(updatedKarma, null, 2));
    return true;
  }
}

module.exports = new DataManager(); 