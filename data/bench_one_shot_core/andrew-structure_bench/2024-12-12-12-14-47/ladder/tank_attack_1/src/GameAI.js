import { AIUtils } from './AIUtils';
import { INITIAL_VALUES, UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'TANK_DAMAGE',
  'TANK_SPEED',
  'TANK_FIRE_RATE',
  'MAX_TANKS',
  'MULTI_SHOT',
  'BASE_COIN_VALUE'
];

export class GameAI {
  constructor() {
    this.ai = new AIUtils();
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
    this.game.coins = Number.MAX_SAFE_INTEGER;

    UPGRADES.forEach(upgrade => {
      const times = Math.floor(Math.random() * 11);
      for (let i = 0; i < times; i++) {
        this.performUpgrade(upgrade, 0, true);
      }
    });

    this.ai.updateDebugOverlay('Experimental mode initialized with random upgrades');
  }

  updateGameStats() {
    const stats = {
      Coins: Math.floor(this.game.coins),
      'Current Tanks': `${this.game.tanks.children.length}/${this.game.maxTanks}`,
      'Tank Damage': this.game.tankDamage.toFixed(1),
      'Tank Speed': this.game.tankSpeed.toFixed(1),
      'Fire Rate': this.game.tankFireRate.toFixed(1),
      'Multi-shot': this.game.multiShot,
      'Base Coin Value': this.game.baseCoinValue.toFixed(1)
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

    for (const upgrade of UPGRADES) {
      const cost = this.game.upgradeCosts[upgrade];
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
    this.upgradeLevels[upgradeName]++;
    const currentLevel = this.upgradeLevels[upgradeName];

    switch (upgradeName) {
      case 'TANK_DAMAGE':
        this.game.upgradeTankDamage();
        break;
      case 'TANK_SPEED':
        this.game.upgradeTankSpeed();
        break;
      case 'TANK_FIRE_RATE':
        this.game.upgradeTankFireRate();
        break;
      case 'MAX_TANKS':
        this.game.upgradeMaxTanks();
        break;
      case 'MULTI_SHOT':
        this.game.upgradeMultiShot();
        break;
      case 'BASE_COIN_VALUE':
        this.game.upgradeBaseCoinValue();
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
