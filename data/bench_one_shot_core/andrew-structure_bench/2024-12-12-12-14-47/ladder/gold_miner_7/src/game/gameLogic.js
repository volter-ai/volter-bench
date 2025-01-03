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
      backgroundColor: 0x000000,
    });

    container.appendChild(this.app.view);

    this.ready = false;
    this.crystals = 0;
    this.droneCount = INITIAL_VALUES.DRONE_COUNT;
    this.miningSpeed = INITIAL_VALUES.MINING_SPEED;
    this.cargoCapacity = INITIAL_VALUES.CARGO_CAPACITY;
    this.asteroidLimit = INITIAL_VALUES.ASTEROID_LIMIT;
    this.crystalDensity = INITIAL_VALUES.CRYSTAL_DENSITY;
    
    this.droneCost = UPGRADE_COSTS.DRONE_COUNT;
    this.miningSpeedCost = UPGRADE_COSTS.MINING_SPEED;
    this.cargoCapacityCost = UPGRADE_COSTS.CARGO_CAPACITY;
    this.asteroidLimitCost = UPGRADE_COSTS.ASTEROID_LIMIT;
    this.crystalDensityCost = UPGRADE_COSTS.CRYSTAL_DENSITY;

    this.lastTimestamp = performance.now();

    // Initialize containers first
    this.drones = new PIXI.Container();
    this.asteroids = new PIXI.Container();

    // Load assets
    this.loadGameAssets();
  }

  loadGameAssets() {
    // Create a PIXI loader
    const loader = PIXI.Loader.shared;
    
    // Add all sprites to the loader
    Object.entries(SPRITES).forEach(([key, sprite]) => {
      loader.add(key, sprite.path);
    });

    // Load everything and then create game objects
    loader.load(() => {
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(spriteConfig) {
    const texture = PIXI.Loader.shared.resources[spriteConfig.name].texture;
    const sprite = new PIXI.Sprite(texture);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite(SPRITES.background);
    
    this.station = this.getSprite(SPRITES.station);
    this.station.anchor.set(0.5);
    this.station.x = SCREEN_SIZE.width / 2;
    this.station.y = SCREEN_SIZE.height / 2;

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.asteroids);
    this.app.stage.addChild(this.drones);
    this.app.stage.addChild(this.station);

    // Create initial drones
    this.createDrone();
    
    // Create initial asteroids
    this.createAsteroid();
  }

  createDrone() {
    const drone = this.getSprite(SPRITES.drone);
    drone.anchor.set(0.5);
    drone.x = this.station.x;
    drone.y = this.station.y;
    drone.state = 'idle';
    drone.cargo = 0;
    drone.miningTimer = 0;
    drone.targetAsteroid = null;
    this.drones.addChild(drone);
  }

  createAsteroid() {
    if (this.asteroids.children.length >= this.asteroidLimit) return;

    const asteroid = this.getSprite(SPRITES.asteroid);
    asteroid.anchor.set(0.5);
    
    do {
      asteroid.x = Math.random() * SCREEN_SIZE.width;
      asteroid.y = Math.random() * SCREEN_SIZE.height;
    } while (Math.hypot(asteroid.x - this.station.x, asteroid.y - this.station.y) < 150);

    asteroid.crystals = this.crystalDensity;
    this.asteroids.addChild(asteroid);
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    // Update drones
    this.drones.children.forEach(drone => {
      switch(drone.state) {
        case 'idle':
          let nearestAsteroid = null;
          let minDistance = Infinity;
          
          this.asteroids.children.forEach(asteroid => {
            if (asteroid.crystals > 0) {
              const dist = Math.hypot(asteroid.x - drone.x, asteroid.y - drone.y);
              if (dist < minDistance) {
                minDistance = dist;
                nearestAsteroid = asteroid;
              }
            }
          });

          if (nearestAsteroid) {
            drone.targetAsteroid = nearestAsteroid;
            drone.state = 'moving_to_mine';
          }
          break;

        case 'moving_to_mine':
          const toMine = this.moveTo(drone, drone.targetAsteroid.x, drone.targetAsteroid.y, elapsedSecs);
          if (toMine) {
            drone.state = 'mining';
            drone.miningTimer = 0;
          }
          break;

        case 'mining':
          drone.miningTimer += elapsedSecs;
          if (drone.miningTimer >= this.miningSpeed) {
            const mineAmount = Math.min(
              this.cargoCapacity - drone.cargo,
              drone.targetAsteroid.crystals
            );
            drone.cargo += mineAmount;
            drone.targetAsteroid.crystals -= mineAmount;
            drone.state = 'returning';

            if (drone.targetAsteroid.crystals <= 0) {
              this.asteroids.removeChild(drone.targetAsteroid);
              this.createAsteroid();
            }
          }
          break;

        case 'returning':
          const toStation = this.moveTo(drone, this.station.x, this.station.y, elapsedSecs);
          if (toStation) {
            this.crystals += drone.cargo;
            drone.cargo = 0;
            drone.state = 'idle';
          }
          break;
      }
    });

    if (this.asteroids.children.length < this.asteroidLimit) {
      this.createAsteroid();
    }
  }

  moveTo(object, targetX, targetY, elapsedSecs) {
    const dx = targetX - object.x;
    const dy = targetY - object.y;
    const distance = Math.hypot(dx, dy);
    
    if (distance < 5) return true;

    const speed = INITIAL_VALUES.DRONE_SPEED * elapsedSecs;
    const movement = Math.min(speed, distance);
    const angle = Math.atan2(dy, dx);
    
    object.x += Math.cos(angle) * movement;
    object.y += Math.sin(angle) * movement;
    object.rotation = angle + Math.PI/2;
    
    return false;
  }

  upgradeDroneCount() {
    if (this.crystals >= this.droneCost) {
      this.crystals -= this.droneCost;
      this.droneCount++;
      this.createDrone();
      this.droneCost *= 2;
    }
  }

  upgradeMiningSpeed() {
    if (this.crystals >= this.miningSpeedCost) {
      this.crystals -= this.miningSpeedCost;
      this.miningSpeed *= 0.9;
      this.miningSpeedCost *= 2;
    }
  }

  upgradeCargoCapacity() {
    if (this.crystals >= this.cargoCapacityCost) {
      this.crystals -= this.cargoCapacityCost;
      this.cargoCapacity = Math.floor(this.cargoCapacity * 1.5);
      this.cargoCapacityCost *= 2;
    }
  }

  upgradeAsteroidLimit() {
    if (this.crystals >= this.asteroidLimitCost) {
      this.crystals -= this.asteroidLimitCost;
      this.asteroidLimit++;
      this.createAsteroid();
      this.asteroidLimitCost *= 2;
    }
  }

  upgradeCrystalDensity() {
    if (this.crystals >= this.crystalDensityCost) {
      this.crystals -= this.crystalDensityCost;
      this.crystalDensity = Math.floor(this.crystalDensity * 1.5);
      this.crystalDensityCost *= 2;
    }
  }

  destroy() {
    this.app.destroy(true);
  }
}
