import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, GAME_CONSTANTS } from './gameData';
import { SPRITES } from './assetManifest';
import { loadAssets } from './utils';
import { EffectsLibrary } from '../lib/effectsLib';

const SCREEN_SIZE = {
  width: 800,
  height: 600
};

export class GameLogic {
  constructor(container) {
    this.app = new PIXI.Application({
      width: SCREEN_SIZE.width,
      height: SCREEN_SIZE.height,
      backgroundColor: 0x000000,
    });

    container.appendChild(this.app.view);

    // Initialize effects library
    this.effects = new EffectsLibrary(this.app);

    this.ready = false;
    this.crystals = 0;
    this.droneCount = INITIAL_VALUES.DRONE_COUNT;
    this.droneSpeed = INITIAL_VALUES.DRONE_SPEED;
    this.cargoCapacity = INITIAL_VALUES.CARGO_CAPACITY;
    this.miningSpeed = INITIAL_VALUES.MINING_SPEED;
    this.maxAsteroids = INITIAL_VALUES.MAX_ASTEROIDS;
    this.asteroidCapacity = INITIAL_VALUES.ASTEROID_CAPACITY;

    this.upgradeCosts = {...UPGRADE_COSTS};
    
    this.asteroidSpawnTimer = 0;
    this.lastTimestamp = performance.now();

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
    
    // Create station container
    this.stationContainer = new PIXI.Container();
    this.station = this.getSprite(SPRITES.station);
    this.station.anchor.set(0.5);
    this.stationContainer.addChild(this.station);
    this.stationContainer.x = SCREEN_SIZE.width / 2;
    this.stationContainer.y = SCREEN_SIZE.height / 2;

    // Create station effects
    this.effects.createShadow(this.stationContainer, this.station, {
      widthRatio: 0.8,
      heightRatio: 0.2,
      alpha: 0.3
    });
    
    const particleSystem = this.effects.createParticleSystem(this.stationContainer, {
      maxParticles: 30,
      radius: 40,
      ellipticalFactor: 0.4
    });

    this.drones = new PIXI.Container();
    this.asteroids = new PIXI.Container();
    this.progressBars = new PIXI.Container();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.asteroids);
    this.app.stage.addChild(this.progressBars);
    this.app.stage.addChild(this.drones);
    this.app.stage.addChild(this.stationContainer);

    this.createInitialDrones();
  }

  createDrone() {
    const droneContainer = new PIXI.Container();
    const drone = this.getSprite(SPRITES.drone);
    drone.anchor.set(0.5);
    droneContainer.addChild(drone);
    
    // Add shadow
    this.effects.createShadow(droneContainer, drone, {
      widthRatio: 0.6,
      heightRatio: 0.2,
      alpha: 0.2
    });

    droneContainer.x = this.stationContainer.x;
    droneContainer.y = this.stationContainer.y;
    droneContainer.state = 'IDLE';
    droneContainer.cargo = 0;
    droneContainer.target = null;
    droneContainer.miningTimer = 0;
    
    this.effects.spawnAnimation(droneContainer);
    this.drones.addChild(droneContainer);
  }

  createAsteroid() {
    const asteroidContainer = new PIXI.Container();
    const asteroid = this.getSprite(SPRITES.asteroid);
    asteroid.anchor.set(0.5);
    asteroidContainer.addChild(asteroid);
    
    // Add shadow
    this.effects.createShadow(asteroidContainer, asteroid, {
      widthRatio: 0.7,
      heightRatio: 0.2,
      alpha: 0.2
    });

    asteroidContainer.x = Math.random() * (SCREEN_SIZE.width - 100) + 50;
    asteroidContainer.y = Math.random() * (SCREEN_SIZE.height - 100) + 50;
    asteroidContainer.crystals = this.asteroidCapacity;
    
    const progressBar = new PIXI.Graphics();
    progressBar.asteroid = asteroidContainer;
    this.progressBars.addChild(progressBar);
    this.updateProgressBar(progressBar);

    this.effects.spawnAnimation(asteroidContainer);
    this.asteroids.addChild(asteroidContainer);
  }

  createInitialDrones() {
    for (let i = 0; i < this.droneCount; i++) {
      this.createDrone();
    }
  }

  updateProgressBar(bar) {
    const asteroid = bar.asteroid;
    const percentage = asteroid.crystals / this.asteroidCapacity;
    
    bar.clear();
    bar.beginFill(0xff0000);
    bar.drawRect(asteroid.x - 25, asteroid.y - 40, 50, 5);
    bar.beginFill(0x00ff00);
    bar.drawRect(asteroid.x - 25, asteroid.y - 40, 50 * percentage, 5);
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.asteroidSpawnTimer += elapsedSecs;
    if (this.asteroidSpawnTimer >= GAME_CONSTANTS.ASTEROID_SPAWN_TIME && 
        this.asteroids.children.length < this.maxAsteroids) {
      this.createAsteroid();
      this.asteroidSpawnTimer = 0;
    }

    this.drones.children.forEach(drone => {
      switch (drone.state) {
        case 'IDLE':
          if (this.asteroids.children.length > 0) {
            drone.target = this.asteroids.children[
              Math.floor(Math.random() * this.asteroids.children.length)
            ];
            drone.state = 'MOVING_TO_ASTEROID';
          }
          break;

        case 'MOVING_TO_ASTEROID':
          if (!drone.target || !this.asteroids.children.includes(drone.target)) {
            drone.state = 'IDLE';
            break;
          }
          
          const dx = drone.target.x - drone.x;
          const dy = drone.target.y - drone.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < 5) {
            drone.state = 'MINING';
            drone.miningTimer = 0;
            this.effects.createImpactEffect(this.app.stage, {
              x: drone.x,
              y: drone.y,
              color: 0x7FFFD4
            });
          } else {
            const speed = this.droneSpeed * elapsedSecs;
            drone.x += (dx / distance) * speed;
            drone.y += (dy / distance) * speed;
            
            // Rotate drone towards movement direction
            drone.rotation = Math.atan2(dy, dx);
          }
          break;

        case 'MINING':
          if (!drone.target || !this.asteroids.children.includes(drone.target)) {
            drone.state = 'IDLE';
            break;
          }

          drone.miningTimer += elapsedSecs;
          
          // Mining effect
          this.effects.createSpiralParticles(this.app.stage, {
            x: drone.x,
            y: drone.y,
            count: 5,
            duration: 0.5
          });

          if (drone.miningTimer >= this.miningSpeed) {
            const mineAmount = Math.min(
              this.cargoCapacity - drone.cargo,
              drone.target.crystals
            );
            
            drone.cargo += mineAmount;
            drone.target.crystals -= mineAmount;
            
            this.effects.showFloatingText(drone, `+${mineAmount}`);
            
            this.updateProgressBar(
              this.progressBars.children.find(bar => bar.asteroid === drone.target)
            );

            if (drone.target.crystals <= 0) {
              const index = this.progressBars.children.findIndex(
                bar => bar.asteroid === drone.target
              );
              this.progressBars.removeChildAt(index);
              
              // Destruction effect
              this.effects.createExplosionParticles(this.app.stage, {
                x: drone.target.x,
                y: drone.target.y,
                color: 0x7FFFD4
              });
              
              this.asteroids.removeChild(drone.target);
            }

            drone.state = 'RETURNING';
          }
          break;

        case 'RETURNING':
          const dxStation = this.stationContainer.x - drone.x;
          const dyStation = this.stationContainer.y - drone.y;
          const distanceStation = Math.sqrt(dxStation * dxStation + dyStation * dyStation);
          
          if (distanceStation < 5) {
            this.crystals += drone.cargo;
            
            // Resource delivery effect
            this.effects.createSpiralParticles(this.app.stage, {
              x: this.stationContainer.x,
              y: this.stationContainer.y,
              count: Math.min(20, drone.cargo),
              duration: 1
            });
            
            this.effects.showFloatingText(this.stationContainer, `+${drone.cargo}`);
            
            drone.cargo = 0;
            drone.state = 'IDLE';
          } else {
            const speed = this.droneSpeed * elapsedSecs;
            drone.x += (dxStation / distanceStation) * speed;
            drone.y += (dyStation / distanceStation) * speed;
            
            // Rotate drone towards movement direction
            drone.rotation = Math.atan2(dyStation, dxStation);
          }
          break;
      }
    });
  }

  upgradeDroneCount() {
    if (this.crystals >= this.upgradeCosts.DRONE_COUNT) {
      this.crystals -= this.upgradeCosts.DRONE_COUNT;
      this.droneCount++;
      this.createDrone();
      this.upgradeCosts.DRONE_COUNT *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 5 });
    }
  }

  upgradeDroneSpeed() {
    if (this.crystals >= this.upgradeCosts.DRONE_SPEED) {
      this.crystals -= this.upgradeCosts.DRONE_SPEED;
      this.droneSpeed *= 1.2;
      this.upgradeCosts.DRONE_SPEED *= 2;
      this.drones.children.forEach(drone => {
        this.effects.flashColor(drone.children[0], { color: 0x00FF00 });
      });
    }
  }

  upgradeCargoCapacity() {
    if (this.crystals >= this.upgradeCosts.CARGO_CAPACITY) {
      this.crystals -= this.upgradeCosts.CARGO_CAPACITY;
      this.cargoCapacity = Math.floor(this.cargoCapacity * 1.5);
      this.upgradeCosts.CARGO_CAPACITY *= 2;
      this.effects.createExplosionParticles(this.app.stage, {
        x: this.stationContainer.x,
        y: this.stationContainer.y,
        color: 0xFFD700
      });
    }
  }

  upgradeMiningSpeed() {
    if (this.crystals >= this.upgradeCosts.MINING_SPEED) {
      this.crystals -= this.upgradeCosts.MINING_SPEED;
      this.miningSpeed *= 0.8;
      this.upgradeCosts.MINING_SPEED *= 2;
      this.drones.children.forEach(drone => {
        this.effects.highlightCharacter(drone.children[0]);
      });
    }
  }

  upgradeMaxAsteroids() {
    if (this.crystals >= this.upgradeCosts.MAX_ASTEROIDS) {
      this.crystals -= this.upgradeCosts.MAX_ASTEROIDS;
      this.maxAsteroids++;
      this.upgradeCosts.MAX_ASTEROIDS *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 8 });
    }
  }

  upgradeAsteroidCapacity() {
    if (this.crystals >= this.upgradeCosts.ASTEROID_CAPACITY) {
      this.crystals -= this.upgradeCosts.ASTEROID_CAPACITY;
      this.asteroidCapacity = Math.floor(this.asteroidCapacity * 1.5);
      this.upgradeCosts.ASTEROID_CAPACITY *= 2;
      this.asteroids.children.forEach(asteroid => {
        this.effects.flashColor(asteroid.children[0], { color: 0xFFD700 });
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
