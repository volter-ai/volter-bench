import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, TRACK_SPACING } from './gameData';
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
    this.coinCount = 0;
    this.runnerSpeed = INITIAL_VALUES.RUNNER_SPEED;
    this.runnerCount = INITIAL_VALUES.RUNNER_COUNT;
    this.trackCount = INITIAL_VALUES.TRACK_COUNT;
    this.coinValue = INITIAL_VALUES.COIN_VALUE;
    this.coinSpawnRate = INITIAL_VALUES.COIN_SPAWN_RATE;
    this.collisionRadius = INITIAL_VALUES.COLLISION_RADIUS;
    
    this.runnerSpeedCost = UPGRADE_COSTS.RUNNER_SPEED;
    this.runnerCountCost = UPGRADE_COSTS.RUNNER_COUNT;
    this.trackCountCost = UPGRADE_COSTS.TRACK_COUNT;
    this.coinValueCost = UPGRADE_COSTS.COIN_VALUE;
    this.coinSpawnRateCost = UPGRADE_COSTS.COIN_SPAWN_RATE;
    this.collisionRadiusCost = UPGRADE_COSTS.COLLISION_RADIUS;

    this.coinSpawnTimer = 0;
    this.obstacleSpawnTimer = 0;
    this.lastTimestamp = performance.now();

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(spriteKey) {
    const texture = PIXI.Texture.from(spriteKey);
    const sprite = new PIXI.Sprite(texture);
    sprite.width = SPRITES[spriteKey].width;
    sprite.height = SPRITES[spriteKey].height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite('background');
    this.runners = new PIXI.Container();
    this.coinContainer = new PIXI.Container();
    this.obstacles = new PIXI.Container();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.coinContainer);
    this.app.stage.addChild(this.obstacles);
    this.app.stage.addChild(this.runners);

    for (let i = 0; i < this.runnerCount; i++) {
      this.createRunner();
    }
  }

  createRunner() {
    const container = new PIXI.Container();
    const sprite = this.getSprite('runner');
    sprite.anchor.set(0.5);
    
    // Add shadow
    this.effects.createShadow(container, sprite);
    
    container.addChild(sprite);
    
    // Add particle trail
    const particleSystem = this.effects.createParticleSystem(container, {
      maxParticles: 20,
      spawnInterval: 5,
      radius: 30
    });
    
    container.x = 0;
    container.y = this.getTrackY(Math.floor(Math.random() * this.trackCount));
    container.currentTrack = Math.floor(container.y / TRACK_SPACING);
    container.sprite = sprite;
    
    // Add idle animation
    this.effects.idleAnimation(sprite);
    
    // Spawn animation
    this.effects.spawnAnimation(container);
    
    this.runners.addChild(container);
  }

  getTrackY(trackIndex) {
    return 100 + trackIndex * TRACK_SPACING;
  }

  spawnCoin() {
    const container = new PIXI.Container();
    const sprite = this.getSprite('coin');
    sprite.anchor.set(0.5);
    container.addChild(sprite);
    
    container.x = SCREEN_SIZE.width;
    container.y = this.getTrackY(Math.floor(Math.random() * this.trackCount));
    
    // Add sparkle effect
    this.effects.createSpiralParticles(container, {
      count: 10,
      duration: 0.5
    });
    
    this.coinContainer.addChild(container);
  }

  spawnObstacle() {
    const container = new PIXI.Container();
    const sprite = this.getSprite('obstacle');
    sprite.anchor.set(0.5);
    container.addChild(sprite);
    
    container.x = SCREEN_SIZE.width;
    container.y = this.getTrackY(Math.floor(Math.random() * this.trackCount));
    
    // Warning flash
    this.effects.flashColor(sprite, {
      color: 0xFF0000,
      flashDuration: 0.3
    });
    
    this.obstacles.addChild(container);
  }

  gameLoop() {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    // Spawn timers
    this.coinSpawnTimer += elapsedSecs;
    if (this.coinSpawnTimer >= 1 / this.coinSpawnRate) {
      this.spawnCoin();
      this.coinSpawnTimer = 0;
    }

    this.obstacleSpawnTimer += elapsedSecs;
    if (this.obstacleSpawnTimer >= INITIAL_VALUES.OBSTACLE_SPAWN_RATE) {
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
        if (Math.abs(obstacle.x - runner.x) < 100 && 
            Math.abs(obstacle.y - runner.y) < TRACK_SPACING) {
          const newTrack = runner.currentTrack + (runner.y > obstacle.y ? 1 : -1);
          if (newTrack >= 0 && newTrack < this.trackCount) {
            const oldY = runner.y;
            runner.y = this.getTrackY(newTrack);
            runner.currentTrack = newTrack;
            
            // Track change effect
            this.effects.lungeAnimation(runner, {
              x: runner.x,
              y: runner.y
            });
          }
        }
      });
    });

    // Move coins and obstacles
    this.coinContainer.children.forEach(coin => {
      coin.x -= 50 * elapsedSecs;
      if (coin.x < 0) {
        this.coinContainer.removeChild(coin);
      }
    });

    this.obstacles.children.forEach(obstacle => {
      obstacle.x -= 50 * elapsedSecs;
      if (obstacle.x < 0) {
        // Destruction effect
        this.effects.createExplosionParticles(this.app.stage, {
          x: obstacle.x,
          y: obstacle.y,
          count: 20
        });
        this.obstacles.removeChild(obstacle);
      }
    });

    // Check coin collection
    this.runners.children.forEach(runner => {
      this.coinContainer.children.forEach(coin => {
        const dx = runner.x - coin.x;
        const dy = runner.y - coin.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < this.collisionRadius) {
          // Collection effects
          this.effects.createSpiralParticles(this.app.stage, {
            x: coin.x,
            y: coin.y,
            count: 15
          });
          
          this.effects.showFloatingText(runner, `+${this.coinValue}`);
          this.effects.flashColor(runner.sprite, {
            color: 0xFFD700
          });
          
          this.coinContainer.removeChild(coin);
          this.coinCount += this.coinValue;
          
          // Milestone effect
          if (Math.floor(this.coinCount) % 100 === 0) {
            this.effects.screenShake(this.app.stage);
          }
        }
      });
    });
  }

  upgradeRunnerSpeed() {
    if (this.coinCount >= this.runnerSpeedCost) {
      this.coinCount -= this.runnerSpeedCost;
      this.runnerSpeed *= 1.2;
      this.runnerSpeedCost *= 2;
      
      // Upgrade effect
      this.runners.children.forEach(runner => {
        this.effects.highlightCharacter(runner.sprite);
      });
    }
  }

  upgradeRunnerCount() {
    if (this.coinCount >= this.runnerCountCost) {
      this.coinCount -= this.runnerCountCost;
      this.runnerCount++;
      this.createRunner();
      this.runnerCountCost *= 2;
    }
  }

  upgradeTrackCount() {
    if (this.coinCount >= this.trackCountCost) {
      this.coinCount -= this.trackCountCost;
      this.trackCount++;
      this.trackCountCost *= 2;
      
      // Track expansion effect
      this.effects.screenShake(this.app.stage, {
        intensity: 5,
        duration: 0.3
      });
    }
  }

  upgradeCoinValue() {
    if (this.coinCount >= this.coinValueCost) {
      this.coinCount -= this.coinValueCost;
      this.coinValue *= 1.5;
      this.coinValueCost *= 2;
    }
  }

  upgradeCoinSpawnRate() {
    if (this.coinCount >= this.coinSpawnRateCost) {
      this.coinCount -= this.coinSpawnRateCost;
      this.coinSpawnRate *= 1.2;
      this.coinSpawnRateCost *= 2;
    }
  }

  upgradeCollisionRadius() {
    if (this.coinCount >= this.collisionRadiusCost) {
      this.coinCount -= this.collisionRadiusCost;
      this.collisionRadius += 5;
      this.collisionRadiusCost *= 2;
      
      // Radius visualization
      this.runners.children.forEach(runner => {
        this.effects.createImpactEffect(runner, {
          radius: this.collisionRadius,
          duration: 0.5,
          alpha: 0.2
        });
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
