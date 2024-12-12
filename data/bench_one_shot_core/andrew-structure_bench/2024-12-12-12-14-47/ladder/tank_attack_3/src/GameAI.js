import { AIUtils } from './AIUtils';
import { UPGRADE_COSTS, INITIAL_VALUES } from './game/gameData';

const UPGRADES = [
  'TANK_COUNT',
  'TANK_DAMAGE', 
  'FIRE_RATE',
  'TANK_HEALTH',
  'TANK_RANGE'
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
      Credits: this.game.credits,
      'Tank Count': this.game.tankCount,
      'Tank Damage': this.game.tankDamage.toFixed(1),
      'Fire Rate': this.game.fireRate.toFixed(1),
      'Tank Health': this.game.tankHealth.toFixed(0),
      'Tank Range': this.game.tankRange.toFixed(0)
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
      'TANK_COUNT': this.game.tankCountCost,
      'TANK_DAMAGE': this.game.tankDamageCost,
      'FIRE_RATE': this.game.fireRateCost,
      'TANK_HEALTH': this.game.tankHealthCost,
      'TANK_RANGE': this.game.tankRangeCost
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
      case 'TANK_COUNT':
        this.game.upgradeTankCount();
        break;
      case 'TANK_DAMAGE':
        this.game.upgradeTankDamage();
        break;
      case 'FIRE_RATE':
        this.game.upgradeFireRate();
        break;
      case 'TANK_HEALTH':
        this.game.upgradeTankHealth();
        break;
      case 'TANK_RANGE':
        this.game.upgradeTankRange();
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
