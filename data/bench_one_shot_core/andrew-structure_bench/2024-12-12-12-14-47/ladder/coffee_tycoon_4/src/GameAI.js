import { AIUtils } from './AIUtils';
import { INITIAL_VALUES, UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'BARISTA',
  'BARISTA_SPEED',
  'CUSTOMER_CAPACITY', 
  'COFFEE_PRICE',
  'PROCESSING_SPEED'
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
      Money: this.game.money,
      'Barista Count': this.game.baristaCount,
      'Customer Count': this.game.customers?.children?.length || 0,
      'Customer Capacity': this.game.customerCapacity,
      'Coffee Price': this.game.coffeePrice,
      'Processing Speed': this.game.processingSpeed.toFixed(2),
      'Barista Speed': this.game.baristaSpeed.toFixed(2),
      'Barista Cost': this.game.baristaCost,
      'Speed Cost': this.game.baristaSpeedCost,
      'Capacity Cost': this.game.customerCapacityCost,
      'Price Cost': this.game.coffeePriceCost,
      'Processing Cost': this.game.processingSpeedCost
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

    const upgradeCosts = {
      BARISTA: this.game.baristaCost,
      BARISTA_SPEED: this.game.baristaSpeedCost,
      CUSTOMER_CAPACITY: this.game.customerCapacityCost,
      COFFEE_PRICE: this.game.coffeePriceCost,
      PROCESSING_SPEED: this.game.processingSpeedCost
    };

    for (const upgrade of UPGRADES) {
      const cost = upgradeCosts[upgrade];
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
      case 'BARISTA':
        this.game.upgradeBarista();
        break;
      case 'BARISTA_SPEED':
        this.game.upgradeBaristaSpeed();
        break;
      case 'CUSTOMER_CAPACITY':
        this.game.upgradeCustomerCapacity();
        break;
      case 'COFFEE_PRICE':
        this.game.upgradeCoffeePrice();
        break;
      case 'PROCESSING_SPEED':
        this.game.upgradeProcessingSpeed();
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
