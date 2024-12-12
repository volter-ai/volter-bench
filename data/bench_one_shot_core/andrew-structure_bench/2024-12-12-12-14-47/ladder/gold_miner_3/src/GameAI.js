import { AIUtils } from './AIUtils';
import { INITIAL_VALUES, UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'DRONE_COUNT',
  'DRONE_SPEED',
  'DRONE_CAPACITY',
  'MAX_ASTEROIDS',
  'ASTEROID_CAPACITY'
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
    return this.game.crystals;
  }

  setupExperimentalMode() {
    // Give infinite currency for experimental mode
    this.game.crystals = Number.MAX_SAFE_INTEGER;

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
      Crystals: this.game.crystals,
      'Drone Count': this.game.droneCount,
      'Drone Speed': this.game.droneSpeed.toFixed(1),
      'Drone Capacity': this.game.droneCapacity,
      'Max Asteroids': this.game.maxAsteroids,
      'Asteroid Capacity': this.game.asteroidCapacity,
      'Drone Cost': this.game.droneCost,
      'Speed Cost': this.game.speedCost,
      'Capacity Cost': this.game.capacityCost,
      'Asteroid Count Cost': this.game.asteroidCountCost,
      'Asteroid Capacity Cost': this.game.asteroidCapacityCost
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
      DRONE_COUNT: this.game.droneCost,
      DRONE_SPEED: this.game.speedCost,
      DRONE_CAPACITY: this.game.capacityCost,
      MAX_ASTEROIDS: this.game.asteroidCountCost,
      ASTEROID_CAPACITY: this.game.asteroidCapacityCost
    };

    for (const upgrade of UPGRADES) {
      const cost = costs[upgrade];
      if (cost <= this.game.crystals && cost < lowestCost) {
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
      case 'DRONE_COUNT':
        this.game.upgradeDroneCount();
        break;
      case 'DRONE_SPEED':
        this.game.upgradeDroneSpeed();
        break;
      case 'DRONE_CAPACITY':
        this.game.upgradeDroneCapacity();
        break;
      case 'MAX_ASTEROIDS':
        this.game.upgradeMaxAsteroids();
        break;
      case 'ASTEROID_CAPACITY':
        this.game.upgradeAsteroidCapacity();
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
