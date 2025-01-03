import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS } from './gameData';
import { SPRITES } from './assetManifest';
import { loadAssets } from './utils';
import { EffectsLibrary } from '../lib/effectsLib';

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
    this.effects = new EffectsLibrary(this.app);

    this.ready = false;
    this.score = 0;
    this.lastTimestamp = performance.now();
    
    // Game values
    this.runnerSpeed = INITIAL_VALUES.RUNNER_SPEED;
    this.coinSpawnRate = INITIAL_VALUES.COIN_SPAWN_RATE;
    this.runnerCount = INITIAL_VALUES.RUNNER_COUNT;
    this.trackCount = INITIAL_VALUES.TRACK_COUNT;
    this.coinValue = INITIAL_VALUES.COIN_VALUE;
    this.collectionRadius = INITIAL_VALUES.COLLECTION_RADIUS;

    // Costs
    this.runnerSpeedCost = UPGRADE_COSTS.RUNNER_SPEED;
    this.coinSpawnRateCost = UPGRADE_COSTS.COIN_SPAWN_RATE;
    this.runnerCountCost = UPGRADE_COSTS.RUNNER_COUNT;
    this.trackCountCost = UPGRADE_COSTS.TRACK_COUNT;
    this.coinValueCost = UPGRADE_COSTS.COIN_VALUE;
    this.collectionRadiusCost = UPGRADE_COSTS.COLLECTION_RADIUS;

    // Timers
    this.coinSpawnTimer = 0;
    this.obstacleSpawnTimer = 0;

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
    this.coinContainer = new PIXI.Container();
    this.obstacles = new PIXI.Container();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.runners);
    this.app.stage.addChild(this.coinContainer);
    this.app.stage.addChild(this.obstacles);

    // Create initial runners
    for (let i = 0; i < this.runnerCount; i++) {
      this.createRunner();
    }
  }

  createRunner() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.runner);
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    // Add shadow
    const shadow = this.effects.createShadow(container, sprite, {
      widthRatio: 0.6,
      heightRatio: 0.2,
      offsetY: 5
    });

    // Add idle animation
    this.effects.idleAnimation(sprite);

    container.x = 0;
    container.y = (SCREEN_SIZE.height / (this.trackCount + 1)) * (Math.floor(Math.random() * this.trackCount) + 1);
    container.currentTrack = Math.floor(container.y / (SCREEN_SIZE.height / (this.trackCount + 1)));
    
    // Spawn animation
    this.effects.spawnAnimation(container);

    this.runners.addChild(container);
  }

  createCoin() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.coin);
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    container.x = SCREEN_SIZE.width;
    container.y = (SCREEN_SIZE.height / (this.trackCount + 1)) * (Math.floor(Math.random() * this.trackCount) + 1);

    // Add spawn animation
    this.effects.spawnAnimation(container, {
      initialScale: { x: 0.5, y: 1.5 },
      finalScale: { x: 1, y: 1 },
      duration: 0.3
    });

    // Add sparkle effect
    this.effects.createParticleSystem(container, {
      maxParticles: 5,
      spawnInterval: 10,
      radius: 20
    });

    this.coinContainer.addChild(container);
  }

  createObstacle() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.obstacle);
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    container.x = SCREEN_SIZE.width;
    container.y = (SCREEN_SIZE.height / (this.trackCount + 1)) * (Math.floor(Math.random() * this.trackCount) + 1);

    // Add spawn animation
    this.effects.spawnAnimation(container, {
      initialScale: { x: 1.5, y: 0.5 },
      finalScale: { x: 1, y: 1 },
      duration: 0.3
    });

    this.obstacles.addChild(container);
  }

  gameLoop(delta) {
    const currentTimestamp = performance.now();
    const elapsedSecs = (currentTimestamp - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTimestamp;

    // Spawn coins
    this.coinSpawnTimer += elapsedSecs;
    if (this.coinSpawnTimer >= this.coinSpawnRate) {
      this.createCoin();
      this.coinSpawnTimer = 0;
    }

    // Spawn obstacles
    this.obstacleSpawnTimer += elapsedSecs;
    if (this.obstacleSpawnTimer >= INITIAL_VALUES.OBSTACLE_SPAWN_RATE) {
      this.createObstacle();
      this.obstacleSpawnTimer = 0;
    }

    // Move runners
    this.runners.children.forEach(runner => {
      runner.x += this.runnerSpeed * elapsedSecs;
      
      // Check for nearby obstacles and avoid
      this.obstacles.children.forEach(obstacle => {
        if (Math.abs(obstacle.x - runner.x) < 100 && runner.currentTrack === Math.floor(obstacle.y / (SCREEN_SIZE.height / (this.trackCount + 1)))) {
          const newTrack = runner.currentTrack + (Math.random() < 0.5 ? 1 : -1);
          if (newTrack >= 0 && newTrack < this.trackCount) {
            runner.currentTrack = newTrack;
            const newY = (SCREEN_SIZE.height / (this.trackCount + 1)) * (runner.currentTrack + 1);
            
            // Add track change effect
            this.effects.createSpiralParticles(this.app.stage, {
              x: runner.x,
              y: runner.y,
              count: 15
            });

            runner.y = newY;
          }
        }
      });

      // Collect coins
      this.coinContainer.children.forEach(coin => {
        const dx = coin.x - runner.x;
        const dy = coin.y - runner.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < this.collectionRadius) {
          // Collection effects
          this.effects.createExplosionParticles(this.app.stage, {
            x: coin.x,
            y: coin.y,
            count: 10,
            color: 0xFFD700
          });
          
          this.effects.showFloatingText(runner, `+${this.coinValue}`, {
            fontSize: 16,
            color: 0xFFD700
          });

          this.coinContainer.removeChild(coin);
          this.score += this.coinValue;
        }
      });

      // Reset runner position
      if (runner.x > SCREEN_SIZE.width) {
        // Despawn effect
        this.effects.createExplosionParticles(this.app.stage, {
          x: runner.x,
          y: runner.y,
          count: 20
        });

        runner.x = 0;
        runner.currentTrack = Math.floor(Math.random() * this.trackCount);
        runner.y = (SCREEN_SIZE.height / (this.trackCount + 1)) * (runner.currentTrack + 1);
        
        // Respawn effect
        this.effects.spawnAnimation(runner);
      }
    });

    // Clean up off-screen objects
    this.coinContainer.children.forEach(coin => {
      if (coin.x < 0) this.coinContainer.removeChild(coin);
    });
    
    this.obstacles.children.forEach(obstacle => {
      if (obstacle.x < 0) this.obstacles.removeChild(obstacle);
    });
  }

  upgradeRunnerSpeed() {
    if (this.score >= this.runnerSpeedCost) {
      this.score -= this.runnerSpeedCost;
      this.runnerSpeed *= 1.2;
      this.runnerSpeedCost *= 2;
      
      // Upgrade effects
      this.runners.children.forEach(runner => {
        this.effects.highlightCharacter(runner.children[0]);
        this.effects.createSpiralParticles(runner, {
          count: 20,
          color: 0x7FFFD4
        });
      });
    }
  }

  upgradeCoinSpawnRate() {
    if (this.score >= this.coinSpawnRateCost) {
      this.score -= this.coinSpawnRateCost;
      this.coinSpawnRate *= 0.8;
      this.coinSpawnRateCost *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 5 });
    }
  }

  upgradeRunnerCount() {
    if (this.score >= this.runnerCountCost) {
      this.score -= this.runnerCountCost;
      this.runnerCount++;
      this.createRunner();
      this.runnerCountCost *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 8 });
    }
  }

  upgradeTrackCount() {
    if (this.score >= this.trackCountCost) {
      this.score -= this.trackCountCost;
      this.trackCount++;
      this.trackCountCost *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 10 });
    }
  }

  upgradeCoinValue() {
    if (this.score >= this.coinValueCost) {
      this.score -= this.coinValueCost;
      this.coinValue *= 1.5;
      this.coinValueCost *= 2;
      
      // Upgrade effect
      this.coinContainer.children.forEach(coin => {
        this.effects.createExplosionParticles(coin, {
          count: 15,
          color: 0xFFD700
        });
      });
    }
  }

  upgradeCollectionRadius() {
    if (this.score >= this.collectionRadiusCost) {
      this.score -= this.collectionRadiusCost;
      this.collectionRadius *= 1.2;
      this.collectionRadiusCost *= 2;
      
      // Upgrade effect
      this.runners.children.forEach(runner => {
        this.effects.createExplosionParticles(runner, {
          count: 20,
          color: 0x7FFFD4
        });
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
