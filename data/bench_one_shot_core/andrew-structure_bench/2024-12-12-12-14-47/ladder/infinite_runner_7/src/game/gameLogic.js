import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS } from './gameData';
import { SPRITES } from './assetManifest';
import { loadAssets } from './utils'

const SCREEN_SIZE = {
  width: 800,
  height: 600
}

export class GameLogic {
  constructor(container) {
    this.app = new PIXI.Application({
      width: SCREEN_SIZE.width,
      height: SCREEN_SIZE.height,
      backgroundColor: 0x222C37,
    });

    container.appendChild(this.app.view);

    this.ready = false;
    this.coins = 0;
    this.lastTimestamp = performance.now();
    
    // Game values
    this.runnerSpeed = INITIAL_VALUES.RUNNER_SPEED;
    this.runnerCount = INITIAL_VALUES.RUNNER_COUNT;
    this.coinSpawnRate = INITIAL_VALUES.COIN_SPAWN_RATE;
    this.coinValue = INITIAL_VALUES.COIN_VALUE;
    this.collectionRadius = INITIAL_VALUES.COLLECTION_RADIUS;

    // Upgrade costs
    this.runnerSpeedCost = UPGRADE_COSTS.RUNNER_SPEED;
    this.runnerCountCost = UPGRADE_COSTS.RUNNER_COUNT;
    this.coinSpawnRateCost = UPGRADE_COSTS.COIN_SPAWN_RATE;
    this.coinValueCost = UPGRADE_COSTS.COIN_VALUE;
    this.collectionRadiusCost = UPGRADE_COSTS.COLLECTION_RADIUS;

    // Timers
    this.coinSpawnTimer = 0;

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(spriteConfig) {
    const texture = PIXI.Texture.from(spriteConfig.path);
    const sprite = new PIXI.Sprite(texture);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite(SPRITES.background);
    this.runners = new PIXI.Container();
    this.coins = new PIXI.Container();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.runners);
    this.app.stage.addChild(this.coins);

    // Create initial runner
    this.createRunner();
  }

  createRunner() {
    const runner = this.getSprite(SPRITES.runner);
    runner.anchor.set(0.5);
    runner.x = 0;
    runner.y = SCREEN_SIZE.height/2 + (Math.random() - 0.5) * 200;
    this.runners.addChild(runner);
  }

  createCoin() {
    const coin = this.getSprite(SPRITES.coin);
    coin.anchor.set(0.5);
    coin.x = Math.random() * SCREEN_SIZE.width;
    coin.y = SCREEN_SIZE.height/2 + (Math.random() - 0.5) * 200;
    this.coins.addChild(coin);
  }

  gameLoop(delta) {
    const currentTimestamp = performance.now();
    const elapsedSecs = (currentTimestamp - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTimestamp;

    // Move runners
    this.runners.children.forEach(runner => {
      runner.x += this.runnerSpeed * elapsedSecs;
      if (runner.x > SCREEN_SIZE.width) {
        runner.x = 0;
      }
    });

    // Spawn coins
    this.coinSpawnTimer += elapsedSecs;
    if (this.coinSpawnTimer >= 1/this.coinSpawnRate) {
      this.createCoin();
      this.coinSpawnTimer = 0;
    }

    // Check coin collection
    this.runners.children.forEach(runner => {
      this.coins.children.forEach(coin => {
        const dx = runner.x - coin.x;
        const dy = runner.y - coin.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < this.collectionRadius) {
          this.coins.removeChild(coin);
          this.coins += this.coinValue;
        }
      });
    });
  }

  upgradeRunnerSpeed() {
    if (this.coins >= this.runnerSpeedCost) {
      this.coins -= this.runnerSpeedCost;
      this.runnerSpeed *= 1.2;
      this.runnerSpeedCost *= 2;
    }
  }

  upgradeRunnerCount() {
    if (this.coins >= this.runnerCountCost) {
      this.coins -= this.runnerCountCost;
      this.runnerCount++;
      this.createRunner();
      this.runnerCountCost *= 2;
    }
  }

  upgradeCoinSpawnRate() {
    if (this.coins >= this.coinSpawnRateCost) {
      this.coins -= this.coinSpawnRateCost;
      this.coinSpawnRate *= 1.2;
      this.coinSpawnRateCost *= 2;
    }
  }

  upgradeCoinValue() {
    if (this.coins >= this.coinValueCost) {
      this.coins -= this.coinValueCost;
      this.coinValue *= 1.5;
      this.coinValueCost *= 2;
    }
  }

  upgradeCollectionRadius() {
    if (this.coins >= this.collectionRadiusCost) {
      this.coins -= this.collectionRadiusCost;
      this.collectionRadius *= 1.2;
      this.collectionRadiusCost *= 2;
    }
  }

  destroy() {
    this.app.destroy(true);
  }
}
