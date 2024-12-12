import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, GAME_CONSTANTS } from './gameData';
import { SPRITES } from './assetManifest';

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
    this.currency = 0;
    this.lastTimestamp = performance.now();
    
    // Game attributes
    this.runnerSpeed = INITIAL_VALUES.RUNNER_SPEED;
    this.runnerCount = INITIAL_VALUES.RUNNER_COUNT;
    this.trackCount = INITIAL_VALUES.TRACK_COUNT;
    this.coinValue = INITIAL_VALUES.COIN_VALUE;
    this.coinSpawnRate = INITIAL_VALUES.COIN_SPAWN_RATE;
    this.collisionRadius = INITIAL_VALUES.COLLISION_RADIUS;

    // Upgrade costs
    this.costs = {...UPGRADE_COSTS};

    // Timers
    this.coinSpawnTimer = 0;
    this.obstacleSpawnTimer = 0;

    // Load assets first
    this.loadAssets();
  }

  loadAssets() {
    // Create loader
    const loader = PIXI.Loader.shared;
    
    // Add all assets to loader
    Object.entries(SPRITES).forEach(([key, sprite]) => {
      loader.add(key, sprite.path);
    });

    // Start loading and create game when done
    loader.load((loader, resources) => {
      this.resources = resources;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });

    // Handle loading errors
    loader.onError.add((error) => {
      console.error("Error loading assets:", error);
    });
  }

  getSprite(spriteConfig) {
    const sprite = new PIXI.Sprite(this.resources[spriteConfig.name].texture);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite({...SPRITES.background, name: 'background'});
    this.runners = new PIXI.Container();
    this.coins = new PIXI.Container();
    this.obstacles = new PIXI.Container();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.runners);
    this.app.stage.addChild(this.coins);
    this.app.stage.addChild(this.obstacles);

    // Create initial runners
    for (let i = 0; i < this.runnerCount; i++) {
      this.createRunner();
    }
  }

  createRunner() {
    const runner = this.getSprite({...SPRITES.runner, name: 'runner'});
    runner.anchor.set(0.5);
    runner.x = 0;
    runner.track = Math.floor(Math.random() * this.trackCount);
    runner.y = GAME_CONSTANTS.TRACK_Y_OFFSET + runner.track * GAME_CONSTANTS.TRACK_SPACING;
    this.runners.addChild(runner);
  }

  spawnCoin() {
    const coin = this.getSprite({...SPRITES.coin, name: 'coin'});
    coin.anchor.set(0.5);
    coin.track = Math.floor(Math.random() * this.trackCount);
    coin.x = SCREEN_SIZE.width;
    coin.y = GAME_CONSTANTS.TRACK_Y_OFFSET + coin.track * GAME_CONSTANTS.TRACK_SPACING;
    this.coins.addChild(coin);
  }

  spawnObstacle() {
    const obstacle = this.getSprite({...SPRITES.obstacle, name: 'obstacle'});
    obstacle.anchor.set(0.5);
    obstacle.track = Math.floor(Math.random() * this.trackCount);
    obstacle.x = SCREEN_SIZE.width;
    obstacle.y = GAME_CONSTANTS.TRACK_Y_OFFSET + obstacle.track * GAME_CONSTANTS.TRACK_SPACING;
    this.obstacles.addChild(obstacle);
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    // Spawn coins
    this.coinSpawnTimer += elapsedSecs;
    if (this.coinSpawnTimer >= 1 / this.coinSpawnRate) {
      this.spawnCoin();
      this.coinSpawnTimer = 0;
    }

    // Spawn obstacles
    this.obstacleSpawnTimer += elapsedSecs;
    if (this.obstacleSpawnTimer >= 1 / GAME_CONSTANTS.OBSTACLE_SPAWN_RATE) {
      this.spawnObstacle();
      this.obstacleSpawnTimer = 0;
    }

    // Move runners
    this.runners.children.forEach(runner => {
      runner.x += this.runnerSpeed * elapsedSecs;
      if (runner.x > SCREEN_SIZE.width) {
        runner.x = 0;
      }

      // Check for nearby obstacles and avoid
      this.obstacles.children.forEach(obstacle => {
        if (Math.abs(obstacle.x - runner.x) < 100 && obstacle.track === runner.track) {
          const newTrack = runner.track + (Math.random() < 0.5 ? 1 : -1);
          if (newTrack >= 0 && newTrack < this.trackCount) {
            runner.track = newTrack;
            runner.y = GAME_CONSTANTS.TRACK_Y_OFFSET + runner.track * GAME_CONSTANTS.TRACK_SPACING;
          }
        }
      });
    });

    // Track items to remove
    const coinsToRemove = [];
    const obstaclesToRemove = [];

    // Move coins and check collection
    this.coins.children.forEach(coin => {
      this.runners.children.forEach(runner => {
        const dx = runner.x - coin.x;
        const dy = runner.y - coin.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < this.collisionRadius) {
          this.currency += this.coinValue;
          coinsToRemove.push(coin);
        }
      });
    });

    // Move obstacles
    this.obstacles.children.forEach(obstacle => {
      obstacle.x -= this.runnerSpeed * elapsedSecs;
      if (obstacle.x < 0) {
        obstaclesToRemove.push(obstacle);
      }
    });

    // Remove collected coins and out-of-bounds obstacles
    coinsToRemove.forEach(coin => {
      if (coin.parent === this.coins) {
        this.coins.removeChild(coin);
      }
    });

    obstaclesToRemove.forEach(obstacle => {
      if (obstacle.parent === this.obstacles) {
        this.obstacles.removeChild(obstacle);
      }
    });
  }

  upgradeRunnerSpeed() {
    if (this.currency >= this.costs.RUNNER_SPEED) {
      this.currency -= this.costs.RUNNER_SPEED;
      this.runnerSpeed *= 1.2;
      this.costs.RUNNER_SPEED *= 2;
    }
  }

  upgradeRunnerCount() {
    if (this.currency >= this.costs.RUNNER_COUNT) {
      this.currency -= this.costs.RUNNER_COUNT;
      this.runnerCount++;
      this.createRunner();
      this.costs.RUNNER_COUNT *= 2;
    }
  }

  upgradeTrackCount() {
    if (this.currency >= this.costs.TRACK_COUNT) {
      this.currency -= this.costs.TRACK_COUNT;
      this.trackCount++;
      this.costs.TRACK_COUNT *= 2;
    }
  }

  upgradeCoinValue() {
    if (this.currency >= this.costs.COIN_VALUE) {
      this.currency -= this.costs.COIN_VALUE;
      this.coinValue *= 1.5;
      this.costs.COIN_VALUE *= 2;
    }
  }

  upgradeCoinSpawnRate() {
    if (this.currency >= this.costs.COIN_SPAWN_RATE) {
      this.currency -= this.costs.COIN_SPAWN_RATE;
      this.coinSpawnRate *= 1.2;
      this.costs.COIN_SPAWN_RATE *= 2;
    }
  }

  upgradeCollisionRadius() {
    if (this.currency >= this.costs.COLLISION_RADIUS) {
      this.currency -= this.costs.COLLISION_RADIUS;
      this.collisionRadius *= 1.2;
      this.costs.COLLISION_RADIUS *= 2;
    }
  }

  destroy() {
    this.app.destroy(true);
  }
}
