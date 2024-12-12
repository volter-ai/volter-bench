import { AIUtils } from './AIUtils';
import { UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'RUNNER_SPEED',
  'COIN_VALUE', 
  'COIN_SPAWN_RATE',
  'RUNNER_COUNT',
  'TRACK_COUNT'
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
    return this.game.coins;
  }

  setupExperimentalMode() {
    // Give infinite currency for experimental mode
    this.game.coins = Number.MAX_SAFE_INTEGER;

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
      Coins: Math.floor(this.game.coins),
      'Runner Count': this.game.runnerCount,
      'Track Count': this.game.trackCount,
      'Runner Speed': this.game.runnerSpeed.toFixed(1),
      'Coin Value': this.game.coinValue.toFixed(1),
      'Spawn Rate': this.game.coinSpawnRate.toFixed(1)
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
      RUNNER_SPEED: this.game.runnerSpeedCost,
      COIN_VALUE: this.game.coinValueCost,
      COIN_SPAWN_RATE: this.game.coinSpawnRateCost,
      RUNNER_COUNT: this.game.runnerCountCost,
      TRACK_COUNT: this.game.trackCountCost
    };

    for (const upgrade of UPGRADES) {
      const cost = costs[upgrade];
      if (cost <= this.game.coins && cost < lowestCost) {
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
      case 'RUNNER_SPEED':
        this.game.upgradeRunnerSpeed();
        break;
      case 'COIN_VALUE':
        this.game.upgradeCoinValue();
        break;
      case 'COIN_SPAWN_RATE':
        this.game.upgradeCoinSpawnRate();
        break;
      case 'RUNNER_COUNT':
        this.game.upgradeRunnerCount();
        break;
      case 'TRACK_COUNT':
        this.game.upgradeTrackCount();
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
