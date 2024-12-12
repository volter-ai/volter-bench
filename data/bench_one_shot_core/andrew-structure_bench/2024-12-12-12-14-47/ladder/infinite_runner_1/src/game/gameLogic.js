import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS } from './gameData';
import { SPRITES } from './assetManifest';
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
    this.score = 0;
    this.runnerSpeed = INITIAL_VALUES.RUNNER_SPEED;
    this.coinSpawnRate = INITIAL_VALUES.COIN_SPAWN_RATE;
    this.coinValue = INITIAL_VALUES.COIN_VALUE;
    this.runnerCount = INITIAL_VALUES.RUNNER_COUNT;
    this.trackWidth = INITIAL_VALUES.TRACK_WIDTH;
    
    this.runnerSpeedCost = UPGRADE_COSTS.RUNNER_SPEED;
    this.coinSpawnRateCost = UPGRADE_COSTS.COIN_SPAWN_RATE;
    this.coinValueCost = UPGRADE_COSTS.COIN_VALUE;
    this.runnerCountCost = UPGRADE_COSTS.RUNNER_COUNT;
    this.trackWidthCost = UPGRADE_COSTS.TRACK_WIDTH;

    this.coinSpawnTimer = 0;
    this.lastTimestamp = performance.now();

    this.textures = {};

    const loader = PIXI.Loader.shared;
    
    if (SPRITES) {
      for (const key in SPRITES) {
        loader.add(key, SPRITES[key].path);
      }
    }

    loader.load((loader, resources) => {
      if (!resources) return;
      
      for (const key in SPRITES) {
        if (resources[key] && resources[key].texture) {
          this.textures[key] = resources[key].texture;
        }
      }

      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(spriteKey) {
    if (!this.textures[spriteKey]) {
      console.error(`Texture not found for key: ${spriteKey}`);
      return new PIXI.Sprite();
    }
    const sprite = new PIXI.Sprite(this.textures[spriteKey]);
    sprite.width = SPRITES[spriteKey].width;
    sprite.height = SPRITES[spriteKey].height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite('background');
    this.runners = new PIXI.Container();
    this.coinsContainer = new PIXI.Container();

    this.createRunner();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.runners);
    this.app.stage.addChild(this.coinsContainer);
  }

  createRunner() {
    const container = new PIXI.Container();
    const sprite = this.getSprite('runner');
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    // Create shadow
    this.effects.createShadow(container, sprite, {
      widthRatio: 0.6,
      heightRatio: 0.2,
      offsetY: 5
    });

    // Add particle system for trail
    const particleSystem = this.effects.createParticleSystem(container, {
      maxParticles: 20,
      spawnInterval: 5,
      radius: 30
    });

    container.x = 0;
    container.y = SCREEN_SIZE.height/2 + (Math.random() - 0.5) * 200;

    // Spawn animation
    this.effects.spawnAnimation(container);
    
    // Idle animation
    this.effects.idleAnimation(container);

    this.runners.addChild(container);
  }

  createCoin() {
    const container = new PIXI.Container();
    const sprite = this.getSprite('coin');
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    // Create shadow
    this.effects.createShadow(container, sprite, {
      widthRatio: 0.4,
      heightRatio: 0.15,
      offsetY: 2
    });

    container.x = Math.random() * this.trackWidth;
    container.y = SCREEN_SIZE.height/2 + (Math.random() - 0.5) * 200;

    // Spawn animation
    this.effects.spawnAnimation(container);

    // Create sparkle effect
    this.effects.createSpiralParticles(container, {
      count: 10,
      duration: 1,
      color: 0xFFD700
    });

    this.coinsContainer.addChild(container);
  }

  gameLoop() {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    if (this.runners && this.runners.children) {
      this.runners.children.forEach(runner => {
        runner.x += this.runnerSpeed * elapsedSecs;
        if (runner.x > SCREEN_SIZE.width) {
          runner.x = 0;
        }
      });
    }

    this.coinSpawnTimer += elapsedSecs;
    if (this.coinSpawnTimer >= 1/this.coinSpawnRate) {
      this.createCoin();
      this.coinSpawnTimer = 0;
    }

    if (this.runners && this.runners.children && this.coinsContainer && this.coinsContainer.children) {
      this.runners.children.forEach(runner => {
        this.coinsContainer.children.forEach(coin => {
          if (this.checkCollision(runner, coin)) {
            // Coin collection effects
            this.effects.createExplosionParticles(this.app.stage, {
              x: coin.x,
              y: coin.y,
              count: 20,
              color: 0xFFD700
            });
            
            this.effects.screenShake(this.app.stage, {
              intensity: 3,
              duration: 0.2
            });

            this.effects.showFloatingText(runner, `+${this.coinValue}`, {
              color: 0xFFD700
            });

            const runnerSprite = runner.children.find(child => child instanceof PIXI.Sprite);
            if (runnerSprite) {
                this.effects.flashColor(runnerSprite, {
                    color: 0xFFD700,
                    duration: 0.2
                });
            }

            this.coinsContainer.removeChild(coin);
            this.score += this.coinValue;
          }
        });
      });
    }
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
      this.runnerSpeed *= 1.2;
      this.runnerSpeedCost *= 2;
      
      // Upgrade effects
      this.runners.children.forEach(runner => {
        const runnerSprite = runner.children.find(child => child instanceof PIXI.Sprite);
        if (runnerSprite) {
            this.effects.highlightCharacter(runnerSprite);
        }
        this.effects.createSpiralParticles(runner, {
          color: 0x00FF00
        });
      });
    }
  }

  upgradeCoinSpawnRate() {
    if (this.score >= this.coinSpawnRateCost) {
      this.score -= this.coinSpawnRateCost;
      this.coinSpawnRate *= 1.2;
      this.coinSpawnRateCost *= 2;

      this.effects.screenShake(this.app.stage, {
        intensity: 5,
        duration: 0.3
      });
    }
  }

  upgradeCoinValue() {
    if (this.score >= this.coinValueCost) {
      this.score -= this.coinValueCost;
      this.coinValue *= 1.5;
      this.coinValueCost *= 2;

      this.coinsContainer.children.forEach(coin => {
        this.effects.createSpiralParticles(coin, {
          color: 0xFFD700
        });
      });
    }
  }

  upgradeRunnerCount() {
    if (this.score >= this.runnerCountCost) {
      this.score -= this.runnerCountCost;
      this.runnerCount++;
      this.createRunner();
      this.runnerCountCost *= 2;

      this.effects.screenShake(this.app.stage, {
        intensity: 8,
        duration: 0.4
      });
    }
  }

  upgradeTrackWidth() {
    if (this.score >= this.trackWidthCost) {
      this.score -= this.trackWidthCost;
      this.trackWidth *= 1.2;
      this.trackWidthCost *= 2;

      this.effects.screenShake(this.app.stage, {
        intensity: 4,
        duration: 0.3
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
