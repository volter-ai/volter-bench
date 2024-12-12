import { AIUtils } from './AIUtils';
import { INITIAL_VALUES, UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'RUNNER_SPEED',
  'RUNNER_COUNT', 
  'COIN_SPAWN_RATE',
  'COIN_VALUE',
  'COLLECTION_RADIUS'
];

const MAX_LOG_ENTRIES = 1000;

export class GameAI {
  constructor() {
    this.ai = null;
    this.game = null;
    this.initialized = false;
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

    try {
      if (this.initialized) return;
      
      this.game = window.game;
      this.ai = new AIUtils();
      
      // Ensure gameLog is initialized
      this.ai.gameLog = [];
      
      // Initialize localStorage safely
      try {
        if (!localStorage.getItem('gameAILogs')) {
          localStorage.setItem('gameAILogs', JSON.stringify({}));
        }
      } catch (error) {
        console.warn('Failed to initialize game logs:', error);
      }

      this.initialized = true;

      if (!this.game.app) return;
      
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

        // Clean up old logs periodically
        setInterval(() => {
          if (this.ai.gameLog && this.ai.gameLog.length > MAX_LOG_ENTRIES) {
            this.ai.gameLog = this.ai.gameLog.slice(-MAX_LOG_ENTRIES);
          }
        }, 5000);

        setTimeout(() => {
          if (this.ai) {
            this.ai.stopAI();
            this.ai.exportLogs();
            this.ai.updateDebugOverlay('Session ended - logs exported');
          }
        }, this.ai.duration);
      }
    } catch (error) {
      console.error('Failed to initialize GameAI:', error);
    }
  }

  getMainCurrency() {
    if (!this.game) return 0;
    return this.game.coins || 0;
  }

  setupExperimentalMode() {
    if (!this.game) return;
    
    this.game.coins = Number.MAX_SAFE_INTEGER;

    UPGRADES.forEach(upgrade => {
      const times = Math.floor(Math.random() * 11);
      for (let i = 0; i < times; i++) {
        this.performUpgrade(upgrade, 0, true);
      }
    });

    if (this.ai) {
      this.ai.updateDebugOverlay('Experimental mode initialized with random upgrades');
    }
  }

  updateGameStats() {
    if (!this.game || !this.ai) return;

    const stats = {
      Coins: Math.floor(this.game.coins || 0),
      'Runner Count': this.game.runnerCount || 0,
      'Runner Speed': (this.game.runnerSpeed || 0).toFixed(1),
      'Spawn Rate': (this.game.coinSpawnRate || 0).toFixed(1),
      'Coin Value': this.game.coinValue || 0,
      'Collection Radius': Math.floor(this.game.collectionRadius || 0)
    };

    this.ai.updateDebugOverlay('Game stats updated', stats);
  }

  startUpgradeLoop() {
    if (!this.ai?.enabled || this.ai?.mode === 'experimental') return;

    this.upgradeInterval = setInterval(() => {
      if (this.game && this.ai) {
        this.checkCheapestUpgrade();
        this.updateGameStats();
      }
    }, 1000);
  }

  checkCheapestUpgrade() {
    if (!this.game) return;

    let cheapestUpgrade = null;
    let lowestCost = Infinity;

    const costs = {
      'RUNNER_SPEED': this.game.runnerSpeedCost,
      'RUNNER_COUNT': this.game.runnerCountCost,
      'COIN_SPAWN_RATE': this.game.coinSpawnRateCost,
      'COIN_VALUE': this.game.coinValueCost,
      'COLLECTION_RADIUS': this.game.collectionRadiusCost
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
    if (!this.game) return;

    this.upgradeLevels[upgradeName]++;
    const currentLevel = this.upgradeLevels[upgradeName];

    try {
      switch (upgradeName) {
        case 'RUNNER_SPEED':
          this.game.upgradeRunnerSpeed();
          break;
        case 'RUNNER_COUNT':
          this.game.upgradeRunnerCount();
          break;
        case 'COIN_SPAWN_RATE':
          this.game.upgradeCoinSpawnRate();
          break;
        case 'COIN_VALUE':
          this.game.upgradeCoinValue();
          break;
        case 'COLLECTION_RADIUS':
          this.game.upgradeCollectionRadius();
          break;
        default:
          console.error(`${upgradeName} is not a valid upgrade`);
      }

      if (!skipLogging && this.ai) {
        const upgradeInfo = {
          timestamp: Date.now(),
          upgrade: upgradeName,
          cost: cost,
          level: currentLevel
        };

        this.ai.logUpgrade(upgradeInfo);
        this.ai.updateDebugOverlay(`Purchased ${upgradeName} upgrade for ${cost} (Level ${currentLevel})`);
      }
    } catch (error) {
      console.warn('Failed to perform upgrade:', error);
    }
  }
}

const gameAI = new GameAI();
gameAI.init();

if (window.game) {
  window.game.exportAILogs = () => gameAI.ai?.exportLogs();
  window.game.clearAILogs = () => gameAI.ai?.clearLogs();
}

export default gameAI;
