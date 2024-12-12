import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, TRACK_CONFIG } from './gameData';
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
    this.score = 0;
    this.runnerSpeed = INITIAL_VALUES.RUNNER_SPEED;
    this.coinSpawnRate = INITIAL_VALUES.COIN_SPAWN_RATE;
    this.coinValue = INITIAL_VALUES.COIN_VALUE;
    this.runnerCount = INITIAL_VALUES.RUNNER_COUNT;
    this.trackCount = INITIAL_VALUES.TRACK_COUNT;
    
    this.runnerSpeedCost = UPGRADE_COSTS.RUNNER_SPEED;
    this.coinSpawnRateCost = UPGRADE_COSTS.COIN_SPAWN_RATE;
    this.coinValueCost = UPGRADE_COSTS.COIN_VALUE;
    this.runnerCountCost = UPGRADE_COSTS.RUNNER_COUNT;
    this.trackCountCost = UPGRADE_COSTS.TRACK_COUNT;

    this.coinSpawnTimer = 0;
    this.lastTimestamp = performance.now();

    // Initialize containers first
    this.runners = new PIXI.Container();
    this.coinContainer = new PIXI.Container();
    this.app.stage.addChild(this.runners);
    this.app.stage.addChild(this.coinContainer);

    // Load assets and create objects after loading
    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(spriteConfig) {
    try {
      const texture = PIXI.Texture.from(spriteConfig.path);
      const sprite = new PIXI.Sprite(texture);
      sprite.width = spriteConfig.width;
      sprite.height = spriteConfig.height;
      return sprite;
    } catch (error) {
      console.error("Error creating sprite:", error);
      return null;
    }
  }

  createGameObjects() {
    // Create and add background first
    const background = this.getSprite(SPRITES.background);
    if (background) {
      this.app.stage.addChildAt(background, 0);
    }

    // Create initial runners
    for (let i = 0; i < this.runnerCount; i++) {
      this.createRunner();
    }
  }

  createRunner() {
    const runner = this.getSprite(SPRITES.runner);
    if (!runner) return;
    
    const trackIndex = this.runners.children.length % this.trackCount;
    runner.anchor.set(0.5);
    runner.x = SCREEN_SIZE.width - runner.width/2;
    runner.y = TRACK_CONFIG.START_Y + (trackIndex * TRACK_CONFIG.SPACING);
    this.runners.addChild(runner);
  }

  spawnCoin() {
    const coin = this.getSprite(SPRITES.coin);
    if (!coin) return;

    coin.anchor.set(0.5);
    const trackIndex = Math.floor(Math.random() * this.trackCount);
    coin.x = Math.random() * (SCREEN_SIZE.width - coin.width) + coin.width/2;
    coin.y = TRACK_CONFIG.START_Y + (trackIndex * TRACK_CONFIG.SPACING);
    this.coinContainer.addChild(coin);
  }

  gameLoop() {
    if (!this.ready) return;

    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    // Move runners
    this.runners.children.forEach(runner => {
      runner.x -= this.runnerSpeed * elapsedSecs;
      if (runner.x < -runner.width/2) {
        runner.x = SCREEN_SIZE.width + runner.width/2;
      }
    });

    // Spawn coins
    this.coinSpawnTimer += elapsedSecs * this.coinSpawnRate;
    while (this.coinSpawnTimer >= 1) {
      this.spawnCoin();
      this.coinSpawnTimer--;
    }

    // Check coin collection
    this.runners.children.forEach(runner => {
      this.coinContainer.children.forEach(coin => {
        if (this.checkCollision(runner, coin)) {
          this.coinContainer.removeChild(coin);
          this.score += this.coinValue;
        }
      });
    });
  }

  checkCollision(obj1, obj2) {
    const dx = obj1.x - obj2.x;
    const dy = obj1.y - obj2.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    return distance < (obj1.width/2 + obj2.width/2);
  }

  upgradeRunnerSpeed() {
    if (this.score >= this.runnerSpeedCost) {
      this.score -= this.runnerSpeedCost;
      this.runnerSpeed *= 1.1;
      this.runnerSpeedCost *= 2;
    }
  }

  upgradeCoinSpawnRate() {
    if (this.score >= this.coinSpawnRateCost) {
      this.score -= this.coinSpawnRateCost;
      this.coinSpawnRate *= 1.1;
      this.coinSpawnRateCost *= 2;
    }
  }

  upgradeCoinValue() {
    if (this.score >= this.coinValueCost) {
      this.score -= this.coinValueCost;
      this.coinValue *= 1.1;
      this.coinValueCost *= 2;
    }
  }

  upgradeRunnerCount() {
    if (this.score >= this.runnerCountCost) {
      this.score -= this.runnerCountCost;
      this.runnerCount++;
      this.createRunner();
      this.runnerCountCost *= 2;
    }
  }

  upgradeTrackCount() {
    if (this.score >= this.trackCountCost && this.trackCount < INITIAL_VALUES.MAX_TRACKS) {
      this.score -= this.trackCountCost;
      this.trackCount++;
      this.trackCountCost *= 2;
    }
  }

  destroy() {
    this.app.destroy(true);
  }
}
