import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS } from './gameData';
import { SPRITES } from './assetManifest';
import { loadAssets } from './utils'

const SCREEN_SIZE = {
  width: 800,
  height: 600
}

const DISTANCE_THRESHOLD = 2; // Added threshold constant

export class GameLogic {
  constructor(container) {
    this.app = new PIXI.Application({
      width: SCREEN_SIZE.width,
      height: SCREEN_SIZE.height,
      backgroundColor: 0x222C37,
    });

    container.appendChild(this.app.view);

    this.ready = false;
    this.crystals = 0;
    this.lastTimestamp = performance.now();

    // Game parameters
    this.droneCount = INITIAL_VALUES.DRONE_COUNT;
    this.miningSpeed = INITIAL_VALUES.MINING_SPEED;
    this.cargoCapacity = INITIAL_VALUES.CARGO_CAPACITY;
    this.droneSpeed = INITIAL_VALUES.DRONE_SPEED;
    this.asteroidRichness = INITIAL_VALUES.ASTEROID_RICHNESS;
    this.maxAsteroids = INITIAL_VALUES.MAX_ASTEROIDS;

    // Upgrade costs
    this.droneCountCost = UPGRADE_COSTS.DRONE_COUNT;
    this.miningSpeedCost = UPGRADE_COSTS.MINING_SPEED;
    this.cargoCapacityCost = UPGRADE_COSTS.CARGO_CAPACITY;
    this.droneSpeedCost = UPGRADE_COSTS.DRONE_SPEED;
    this.asteroidRichnessCost = UPGRADE_COSTS.ASTEROID_RICHNESS;
    this.maxAsteroidsCost = UPGRADE_COSTS.MAX_ASTEROIDS;

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
    this.app.stage.addChild(this.background);

    // Create containers
    this.drones = new PIXI.Container();
    this.asteroids = new PIXI.Container();
    
    // Create station
    this.station = this.getSprite(SPRITES.station);
    this.station.anchor.set(0.5);
    this.station.x = SCREEN_SIZE.width / 2;
    this.station.y = SCREEN_SIZE.height / 2;

    // Create initial drones and asteroids
    this.createDrone();
    for (let i = 0; i < this.maxAsteroids; i++) {
      this.createAsteroid();
    }

    this.app.stage.addChild(this.asteroids);
    this.app.stage.addChild(this.station);
    this.app.stage.addChild(this.drones);
  }

  createDrone() {
    const drone = this.getSprite(SPRITES.drone);
    drone.anchor.set(0.5);
    drone.x = this.station.x;
    drone.y = this.station.y;
    drone.cargo = 0;
    drone.miningTimer = 0;
    drone.target = null;
    drone.state = 'seeking'; // seeking, mining, returning
    this.drones.addChild(drone);
  }

  createAsteroid() {
    const asteroid = this.getSprite(SPRITES.asteroid);
    asteroid.anchor.set(0.5);
    
    // Keep spawning away from station
    do {
      asteroid.x = Math.random() * this.app.screen.width;
      asteroid.y = Math.random() * this.app.screen.height;
    } while (this.getDistance(asteroid, this.station) < 100);

    asteroid.crystals = this.asteroidRichness;
    asteroid.maxCrystals = this.asteroidRichness;
    asteroid.targeted = false;  // Initialize targeted flag
    
    // Create progress bar
    const bar = new PIXI.Graphics();
    bar.beginFill(0x00ff00);
    bar.drawRect(-32, -40, 64, 5);
    bar.endFill();
    asteroid.addChild(bar);
    asteroid.progressBar = bar;
    
    this.asteroids.addChild(asteroid);
  }

  getDistance(obj1, obj2) {
    const dx = obj1.x - obj2.x;
    const dy = obj1.y - obj2.y;
    return Math.sqrt(dx * dx + dy * dy);
  }

  findNearestAsteroid(drone) {
    let nearest = null;
    let minDistance = Infinity;
    
    this.asteroids.children.forEach(asteroid => {
      const distance = this.getDistance(drone, asteroid);
      if (distance < minDistance && !asteroid.targeted) {
        minDistance = distance;
        nearest = asteroid;
      }
    });
    
    if (nearest) nearest.targeted = true;
    return nearest;
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.drones.children.forEach(drone => {
      switch(drone.state) {
        case 'seeking':
          if (!drone.target) {
            drone.target = this.findNearestAsteroid(drone);
          }
          if (drone.target) {
            this.moveDrone(drone, drone.target, elapsedSecs);
            if (this.getDistance(drone, drone.target) < DISTANCE_THRESHOLD) {
              drone.state = 'mining';
            }
          }
          break;

        case 'mining':
          drone.miningTimer += elapsedSecs;
          if (drone.miningTimer >= this.miningSpeed) {
            drone.miningTimer = 0;
            if (drone.target.crystals > 0 && drone.cargo < this.cargoCapacity) {
              drone.cargo++;
              drone.target.crystals--;
              drone.target.progressBar.width = (drone.target.crystals / drone.target.maxCrystals) * 64;
            }
            if (drone.cargo >= this.cargoCapacity || drone.target.crystals <= 0) {
              drone.state = 'returning';
              if (drone.target.crystals <= 0) {
                drone.target.targeted = false;  // Clear targeted flag before removal
                this.asteroids.removeChild(drone.target);
                this.createAsteroid();
              } else {
                drone.target.targeted = false;  // Clear targeted flag if asteroid still exists
              }
              drone.target = null;
            }
          }
          break;

        case 'returning':
          this.moveDrone(drone, this.station, elapsedSecs);
          if (this.getDistance(drone, this.station) < DISTANCE_THRESHOLD) {
            this.crystals += drone.cargo;
            drone.cargo = 0;
            drone.state = 'seeking';
            drone.target = null;  // Explicitly clear target when returning to seeking state
          }
          break;
      }
    });
  }

  moveDrone(drone, target, elapsedSecs) {
    const dx = target.x - drone.x;
    const dy = target.y - drone.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance > DISTANCE_THRESHOLD) {
      const moveDistance = this.droneSpeed * elapsedSecs;
      const vx = (dx / distance) * moveDistance;
      const vy = (dy / distance) * moveDistance;
      
      drone.x += vx;
      drone.y += vy;
      drone.rotation = Math.atan2(dy, dx) + Math.PI/2;
    }
  }

  upgradeDroneCount() {
    if (this.crystals >= this.droneCountCost) {
      this.crystals -= this.droneCountCost;
      this.droneCount++;
      this.createDrone();
      this.droneCountCost *= 2;
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
      this.cargoCapacity = Math.floor(this.cargoCapacity * 1.2);
      this.cargoCapacityCost *= 2;
    }
  }

  upgradeDroneSpeed() {
    if (this.crystals >= this.droneSpeedCost) {
      this.crystals -= this.droneSpeedCost;
      this.droneSpeed *= 1.2;
      this.droneSpeedCost *= 2;
    }
  }

  upgradeAsteroidRichness() {
    if (this.crystals >= this.asteroidRichnessCost) {
      this.crystals -= this.asteroidRichnessCost;
      this.asteroidRichness = Math.floor(this.asteroidRichness * 1.3);
      this.asteroidRichnessCost *= 2;
    }
  }

  upgradeMaxAsteroids() {
    if (this.crystals >= this.maxAsteroidsCost) {
      this.crystals -= this.maxAsteroidsCost;
      this.maxAsteroids++;
      this.createAsteroid();
      this.maxAsteroidsCost *= 2;
    }
  }

  destroy() {
    this.app.destroy(true);
  }
}
