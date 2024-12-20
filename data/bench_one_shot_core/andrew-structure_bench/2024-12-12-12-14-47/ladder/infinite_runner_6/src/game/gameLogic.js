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

    // Initialize effects library
    this.effects = new EffectsLibrary(this.app);

    this.ready = false;
    this.coins = 0;
    this.lastTimestamp = performance.now();
    
    // Game values
    this.runnerSpeed = INITIAL_VALUES.RUNNER_SPEED;
    this.coinValue = INITIAL_VALUES.COIN_VALUE;
    this.coinSpawnRate = INITIAL_VALUES.COIN_SPAWN_RATE;
    this.runnerCount = INITIAL_VALUES.RUNNER_COUNT;
    this.trackCount = INITIAL_VALUES.TRACK_COUNT;
    
    // Upgrade costs
    this.runnerSpeedCost = UPGRADE_COSTS.RUNNER_SPEED;
    this.coinValueCost = UPGRADE_COSTS.COIN_VALUE;
    this.coinSpawnRateCost = UPGRADE_COSTS.COIN_SPAWN_RATE;
    this.runnerCountCost = UPGRADE_COSTS.RUNNER_COUNT;
    this.trackCountCost = UPGRADE_COSTS.TRACK_COUNT;

    // Timers
    this.coinSpawnTimer = 0;

    // Initialize containers
    this.runners = new PIXI.Container();
    this.coinContainer = new PIXI.Container();
    
    this.app.stage.addChild(this.runners);
    this.app.stage.addChild(this.coinContainer);

    // Load assets before creating sprites
    PIXI.Loader.shared.reset();
    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      
      // Create background first
      this.background = this.getSprite(SPRITES.background);
      this.app.stage.addChildAt(this.background, 0);
      
      // Create initial runners
      for (let i = 0; i < this.runnerCount; i++) {
        this.createRunner();
      }
      
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

  getTrackY(trackIndex) {
    return 100 + (trackIndex * INITIAL_VALUES.TRACK_SPACING);
  }

  createRunner() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.runner);
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    // Add shadow
    const shadow = this.effects.createShadow(container, sprite, {
      offsetY: 5
    });
    
    // Position the container
    container.x = Math.random() * this.app.screen.width;
    container.y = this.getTrackY(Math.floor(Math.random() * this.trackCount));

    // Add idle animation to shadow
    this.effects.idleAnimation(shadow);

    // Spawn animation
    this.effects.spawnAnimation(container);

    // Create particle system for trail
    const particleSystem = this.effects.createParticleSystem(container, {
      maxParticles: 15,
      spawnInterval: 5,
      radius: 2
    });

    container.particleSystem = particleSystem;
    this.runners.addChild(container);
  }

  spawnCoin() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.coin);
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    // Position the container
    container.x = Math.random() * this.app.screen.width;
    container.y = this.getTrackY(Math.floor(Math.random() * this.trackCount));

    // Add spawn animation
    this.effects.spawnAnimation(container, {
      initialScale: { x: 0.3, y: 1.5 },
      finalScale: { x: 1, y: 1 },
      duration: 0.5
    });

    // Add sparkle effect
    const particleSystem = this.effects.createParticleSystem(container, {
      maxParticles: 5,
      spawnInterval: 10,
      radius: 15,
      ellipticalFactor: 1
    });

    container.particleSystem = particleSystem;
    this.coinContainer.addChild(container);
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    // Move runners
    this.runners.children.forEach(runner => {
      runner.x += this.runnerSpeed * elapsedSecs;
      if (runner.x > this.app.screen.width + runner.width/2) {
        runner.x = -runner.width/2;
      }
      
      // Update particle system
      if (runner.particleSystem) {
        runner.particleSystem.update(delta);
      }
    });

    // Update coin particle systems
    this.coinContainer.children.forEach(coin => {
      if (coin.particleSystem) {
        coin.particleSystem.update(delta);
      }
    });

    // Spawn coins
    this.coinSpawnTimer += elapsedSecs;
    if (this.coinSpawnTimer >= 1/this.coinSpawnRate) {
      this.spawnCoin();
      this.coinSpawnTimer = 0;
    }

    // Check collisions
    this.runners.children.forEach(runner => {
      this.coinContainer.children.forEach(coin => {
        if (this.checkCollision(runner, coin)) {
          // Collection effects
          this.effects.createExplosionParticles(this.app.stage, {
            x: coin.x,
            y: coin.y,
            count: 20,
            color: 0xFFD700
          });
          
          this.effects.showFloatingText(runner, `+${this.coinValue}`, {
            fontSize: 16,
            color: 0xFFD700
          });
          
          this.effects.screenShake(this.app.stage, {
            intensity: 3,
            duration: 0.2
          });
          
          // Instead of flashColor, use highlightCharacter which is more reliable
          this.effects.highlightCharacter(runner.children[0], {
            color: 0xFFD700,
            duration: 0.1
          });

          this.coins += this.coinValue;
          this.coinContainer.removeChild(coin);
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
    if (this.coins >= this.runnerSpeedCost) {
      this.coins -= this.runnerSpeedCost;
      this.runnerSpeed *= 1.2;
      this.runnerSpeedCost *= 2;
      
      // Highlight all runners
      this.runners.children.forEach(runner => {
        this.effects.highlightCharacter(runner.children[0], {
          color: 0x00FF00,
          duration: 0.5
        });
      });
    }
  }

  upgradeCoinValue() {
    if (this.coins >= this.coinValueCost) {
      this.coins -= this.coinValueCost;
      this.coinValue *= 1.5;
      this.coinValueCost *= 2;
      
      // Effect on all coins
      this.coinContainer.children.forEach(coin => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: coin.x,
          y: coin.y
        });
      });
    }
  }

  upgradeCoinSpawnRate() {
    if (this.coins >= this.coinSpawnRateCost) {
      this.coins -= this.coinSpawnRateCost;
      this.coinSpawnRate *= 1.3;
      this.coinSpawnRateCost *= 2;
      
      this.effects.screenShake(this.app.stage, {
        intensity: 5,
        duration: 0.3
      });
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

  upgradeTrackCount() {
    if (this.coins >= this.trackCountCost && this.trackCount < INITIAL_VALUES.MAX_TRACKS) {
      this.coins -= this.trackCountCost;
      this.trackCount++;
      this.trackCountCost *= 2;
      
      // Track creation effect
      const newTrackY = this.getTrackY(this.trackCount - 1);
      this.effects.createSpiralParticles(this.app.stage, {
        x: this.app.screen.width / 2,
        y: newTrackY,
        count: 30,
        duration: 1.5
      });
      
      this.effects.screenShake(this.app.stage, {
        intensity: 8,
        duration: 0.4
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
