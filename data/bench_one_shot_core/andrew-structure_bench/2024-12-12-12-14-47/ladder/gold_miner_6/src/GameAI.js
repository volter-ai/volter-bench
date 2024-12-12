import { AIUtils } from './AIUtils';
import { INITIAL_VALUES, UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'DRONE_COUNT',
  'MINING_SPEED', 
  'CARGO_CAPACITY',
  'DRONE_SPEED',
  'ASTEROID_RICHNESS',
  'MAX_ASTEROIDS'
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
      'Mining Speed': this.game.miningSpeed.toFixed(2),
      'Cargo Capacity': this.game.cargoCapacity,
      'Drone Speed': Math.floor(this.game.droneSpeed),
      'Asteroid Richness': this.game.asteroidRichness,
      'Max Asteroids': this.game.maxAsteroids,
      // Costs
      'Drone Cost': this.game.droneCountCost,
      'Mining Speed Cost': this.game.miningSpeedCost,
      'Cargo Cost': this.game.cargoCapacityCost,
      'Speed Cost': this.game.droneSpeedCost,
      'Richness Cost': this.game.asteroidRichnessCost,
      'Max Asteroids Cost': this.game.maxAsteroidsCost
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
      DRONE_COUNT: this.game.droneCountCost,
      MINING_SPEED: this.game.miningSpeedCost,
      CARGO_CAPACITY: this.game.cargoCapacityCost,
      DRONE_SPEED: this.game.droneSpeedCost,
      ASTEROID_RICHNESS: this.game.asteroidRichnessCost,
      MAX_ASTEROIDS: this.game.maxAsteroidsCost
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
      case 'MINING_SPEED':
        this.game.upgradeMiningSpeed();
        break;
      case 'CARGO_CAPACITY':
        this.game.upgradeCargoCapacity();
        break;
      case 'DRONE_SPEED':
        this.game.upgradeDroneSpeed();
        break;
      case 'ASTEROID_RICHNESS':
        this.game.upgradeAsteroidRichness();
        break;
      case 'MAX_ASTEROIDS':
        this.game.upgradeMaxAsteroids();
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
