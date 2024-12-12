import { AIUtils } from './AIUtils';
import { INITIAL_VALUES, UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'BALL_SPEED',
  'PADDLE_SIZE',
  'BALL_COUNT',
  'PADDLE_SPEED',
  'POINTS_MULTIPLIER'
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
    return this.game.score;
  }

  setupExperimentalMode() {
    // Give infinite currency for experimental mode
    this.game.score = Number.MAX_SAFE_INTEGER;

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
      Score: this.game.score,
      'Ball Speed': this.game.ballSpeed,
      'Paddle Size': this.game.paddleSize,
      'Ball Count': this.game.ballCount,
      'Paddle Speed': this.game.paddleSpeed,
      'Points Multiplier': this.game.pointsMultiplier,
      'Ball Speed Cost': this.game.ballSpeedCost,
      'Paddle Size Cost': this.game.paddleSizeCost,
      'Ball Count Cost': this.game.ballCountCost,
      'Paddle Speed Cost': this.game.paddleSpeedCost,
      'Points Multiplier Cost': this.game.pointsMultiplierCost
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
    const upgradeCosts = {
      BALL_SPEED: this.game.ballSpeedCost,
      PADDLE_SIZE: this.game.paddleSizeCost,
      BALL_COUNT: this.game.ballCountCost,
      PADDLE_SPEED: this.game.paddleSpeedCost,
      POINTS_MULTIPLIER: this.game.pointsMultiplierCost
    };

    let cheapestUpgrade = null;
    let lowestCost = Infinity;

    for (const upgrade in upgradeCosts) {
      const cost = upgradeCosts[upgrade];
      if (cost <= this.game.score && cost < lowestCost) {
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
      case 'BALL_SPEED':
        this.game.upgradeBallSpeed();
        break;
      case 'PADDLE_SIZE':
        this.game.upgradePaddleSize();
        break;
      case 'BALL_COUNT':
        this.game.upgradeBallCount();
        break;
      case 'PADDLE_SPEED':
        this.game.upgradePaddleSpeed();
        break;
      case 'POINTS_MULTIPLIER':
        this.game.upgradePointsMultiplier();
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
