import { AIUtils } from './AIUtils';
import { UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'TANK_HEALTH',
  'TANK_DAMAGE', 
  'TANK_SPEED',
  'TANK_COUNT',
  'BASE_REWARD'
];

export class GameAI {
  constructor() {
    this.ai = new AIUtils();
    this.game = null;
    this.initialized = false;
    // Initialize upgrade levels for all upgrade types
    this.upgradeLevels = UPGRADES.reduce((acc, upgrade) => {
      acc[upgrade] = 0;
      return acc;
    }, {});
  }

  init() {
    if (!window.game || !window.game.ready) {
      setTimeout(() => this.init(), 100);
      return;
    }
    this.game = window.game;

    if (this.initialized) return;
    this.initialized = true;

    window.game.app.ticker.speed = this.ai.defaultGameSpeed;
    this.ai.updateDebugOverlay('Game speed set to ' + this.ai.defaultGameSpeed + 'x');

    if (this.ai.enabled) {
      this.ai.gameStartTime = Date.now();

      if (this.ai.mode === 'experimental') {
        this.setupExperimentalMode();
      }

      this.ai.startLoggingLoop(this.getMainCurrency.bind(this));
      this.startUpgradeLoop();
      this.updateGameStats();

      setTimeout(() => {
        this.ai.stopAI();
        this.ai.exportLogs();
        this.ai.updateDebugOverlay('Session ended - logs exported');
      }, this.ai.duration);
    }
  }

  getMainCurrency() {
    return this.game.credits;
  }

  setupExperimentalMode() {
    // Give infinite currency for experimental mode
    this.game.credits = Number.MAX_SAFE_INTEGER;

    // Randomly upgrade each stat between 0-10 times
    UPGRADES.forEach(upgrade => {
      const times = Math.floor(Math.random() * 11); // 0 to 10
      for (let i = 0; i < times; i++) {
        this.performUpgrade(upgrade, 0, true);
      }
    });

    this.ai.updateDebugOverlay('Experimental mode initialized with random upgrades');
  }

  updateGameStats() {
    const stats = {
      Credits: Math.floor(this.game.credits),
      'Tank Count': this.game.tankCount,
      'Tank Health': Math.floor(this.game.tankHealth),
      'Tank Damage': Math.floor(this.game.tankDamage),
      'Tank Speed': Math.floor(this.game.tankSpeed),
      'Base Reward': Math.floor(this.game.baseReward),
      'Tank Health Level': this.upgradeLevels.TANK_HEALTH,
      'Tank Damage Level': this.upgradeLevels.TANK_DAMAGE,
      'Tank Speed Level': this.upgradeLevels.TANK_SPEED,
      'Tank Count Level': this.upgradeLevels.TANK_COUNT,
      'Base Reward Level': this.upgradeLevels.BASE_REWARD
    };

    this.ai.updateDebugOverlay('Game stats updated', stats);
  }

  startUpgradeLoop() {
    if (!this.ai.enabled || this.ai.mode === 'experimental') return;

    this.upgradeInterval = setInterval(() => {
      this.checkCheapestUpgrade();
      this.updateGameStats();
    }, 100);
  }

  checkCheapestUpgrade() {
    let cheapestUpgrade = null;
    let lowestCost = Infinity;

    const costs = {
      TANK_HEALTH: this.game.tankHealthCost,
      TANK_DAMAGE: this.game.tankDamageCost,
      TANK_SPEED: this.game.tankSpeedCost,
      TANK_COUNT: this.game.tankCountCost,
      BASE_REWARD: this.game.baseRewardCost
    };

    for (const upgrade of UPGRADES) {
      const cost = costs[upgrade];
      if (cost <= this.game.credits && cost < lowestCost) {
        cheapestUpgrade = upgrade;
        lowestCost = cost;
      }
    }

    if (cheapestUpgrade) {
      this.performUpgrade(cheapestUpgrade, lowestCost);
    }
  }

  performUpgrade(upgradeName, cost, skipLogging = false) {
    // Increment the upgrade level before performing the upgrade
    this.upgradeLevels[upgradeName]++;
    const currentLevel = this.upgradeLevels[upgradeName];

    switch (upgradeName) {
      case 'TANK_HEALTH':
        this.game.upgradeTankHealth();
        break;
      case 'TANK_DAMAGE':
        this.game.upgradeTankDamage();
        break;
      case 'TANK_SPEED':
        this.game.upgradeTankSpeed();
        break;
      case 'TANK_COUNT':
        this.game.upgradeTankCount();
        break;
      case 'BASE_REWARD':
        this.game.upgradeBaseReward();
        break;
      default:
        console.error(`${upgradeName} is not a valid upgrade`);
    }

    if (!skipLogging) {
      const upgradeInfo = {
        timestamp: Date.now(),
        upgrade: upgradeName,
        cost: cost,
        level: currentLevel
      };

      this.ai.logUpgrade(upgradeInfo);
      this.ai.updateDebugOverlay(`Purchased ${upgradeName} upgrade for ${cost} (Level ${currentLevel})`);
    }
  }
}

const gameAI = new GameAI();
gameAI.init();

if (window.game) {
  window.game.exportAILogs = () => gameAI.ai.exportLogs();
  window.game.clearAILogs = () => gameAI.ai.clearLogs();
}

export default gameAI;
