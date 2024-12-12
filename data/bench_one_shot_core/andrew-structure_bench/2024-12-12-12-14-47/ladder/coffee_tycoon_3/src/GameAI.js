import { AIUtils } from './AIUtils';
import { INITIAL_VALUES, UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'COFFEE_PRICE',
  'COFFEE_SPEED',
  'BARISTA_COUNT', 
  'CUSTOMER_CAPACITY',
  'BARISTA_EFFICIENCY'
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
    return this.game.money;
  }

  setupExperimentalMode() {
    // Give infinite money for experimental mode
    this.game.money = Number.MAX_SAFE_INTEGER;

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
      Money: Math.floor(this.game.money),
      'Coffee Price': this.game.coffeePrice.toFixed(2),
      'Make Speed': this.game.coffeeMakeSpeed.toFixed(1) + 's',
      'Barista Count': this.game.baristaCount,
      'Customer Capacity': this.game.customerCapacity,
      'Barista Efficiency': this.game.baristaEfficiency,
      'Price Upgrade Cost': this.game.coffeePriceCost,
      'Speed Upgrade Cost': this.game.coffeeSpeedCost,
      'Barista Hire Cost': this.game.baristaCountCost,
      'Capacity Upgrade Cost': this.game.customerCapacityCost,
      'Efficiency Upgrade Cost': this.game.baristaEfficiencyCost
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
      'COFFEE_PRICE': this.game.coffeePriceCost,
      'COFFEE_SPEED': this.game.coffeeSpeedCost,
      'BARISTA_COUNT': this.game.baristaCountCost,
      'CUSTOMER_CAPACITY': this.game.customerCapacityCost,
      'BARISTA_EFFICIENCY': this.game.baristaEfficiencyCost
    };

    for (const upgrade of UPGRADES) {
      const cost = costs[upgrade];
      if (cost <= this.game.money && cost < lowestCost) {
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
      case 'COFFEE_PRICE':
        this.game.upgradeCoffeePrice();
        break;
      case 'COFFEE_SPEED':
        this.game.upgradeCoffeeSpeed();
        break;
      case 'BARISTA_COUNT':
        this.game.upgradeBaristaCount();
        break;
      case 'CUSTOMER_CAPACITY':
        this.game.upgradeCustomerCapacity();
        break;
      case 'BARISTA_EFFICIENCY':
        this.game.upgradeBaristaEfficiency();
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
