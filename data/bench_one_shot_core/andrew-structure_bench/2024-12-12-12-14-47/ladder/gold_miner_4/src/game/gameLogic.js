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
      backgroundColor: 0x000000,
    });

    container.appendChild(this.app.view);

    this.effects = new EffectsLibrary(this.app);
    this.ready = false;
    this.crystals = 0;
    this.droneCount = INITIAL_VALUES.DRONE_COUNT;
    this.droneSpeed = INITIAL_VALUES.DRONE_SPEED;
    this.droneCargo = INITIAL_VALUES.DRONE_CARGO;
    this.asteroidCapacity = INITIAL_VALUES.ASTEROID_CAPACITY;
    this.maxAsteroids = INITIAL_VALUES.MAX_ASTEROIDS;
    
    this.droneCountCost = UPGRADE_COSTS.DRONE_COUNT;
    this.droneSpeedCost = UPGRADE_COSTS.DRONE_SPEED;
    this.droneCargoCost = UPGRADE_COSTS.DRONE_CARGO;
    this.asteroidCapacityCost = UPGRADE_COSTS.ASTEROID_CAPACITY;
    this.maxAsteroidsCost = UPGRADE_COSTS.MAX_ASTEROIDS;

    this.drones = new PIXI.Container();
    this.asteroids = new PIXI.Container();

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(spriteKey, spriteConfig) {
    const texture = PIXI.Loader.shared.resources[spriteKey].texture;
    const sprite = new PIXI.Sprite(texture);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite('background', SPRITES.background);
    
    // Create station container and effects
    this.station = new PIXI.Container();
    const stationSprite = this.getSprite('station', SPRITES.station);
    stationSprite.anchor.set(0.5);
    this.station.addChild(stationSprite);
    this.station.x = SCREEN_SIZE.width / 2;
    this.station.y = SCREEN_SIZE.height / 2;
    
    // Add station effects
    this.effects.createShadow(this.station, stationSprite);
    this.effects.idleAnimation(this.station);
    const stationAura = this.effects.createParticleSystem(this.station, {
      maxParticles: 20,
      radius: 40,
      spawnInterval: 3
    });

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.asteroids);
    this.app.stage.addChild(this.station);
    this.app.stage.addChild(this.drones);

    for (let i = 0; i < this.droneCount; i++) {
      this.createDrone();
    }

    for (let i = 0; i < this.maxAsteroids; i++) {
      this.createAsteroid();
    }
  }

  createDrone() {
    const droneContainer = new PIXI.Container();
    const droneSprite = this.getSprite('drone', SPRITES.drone);
    droneSprite.anchor.set(0.5);
    droneContainer.addChild(droneSprite);
    
    // Add drone effects
    this.effects.createShadow(droneContainer, droneSprite);
    this.effects.idleAnimation(droneContainer);
    
    droneContainer.x = this.station.x;
    droneContainer.y = this.station.y;
    droneContainer.cargo = 0;
    droneContainer.state = 'seeking';
    droneContainer.targetAsteroid = null;
    droneContainer.miningTimer = 0;
    droneContainer.sprite = droneSprite;
    
    this.drones.addChild(droneContainer);
    
    // Spawn animation
    this.effects.spawnAnimation(droneContainer);
  }

  createAsteroid() {
    const asteroidContainer = new PIXI.Container();
    const asteroidSprite = this.getSprite('asteroid', SPRITES.asteroid);
    asteroidSprite.anchor.set(0.5);
    asteroidContainer.addChild(asteroidSprite);
    
    // Add asteroid effects
    this.effects.createShadow(asteroidContainer, asteroidSprite);
    this.effects.idleAnimation(asteroidContainer);
    
    do {
      asteroidContainer.x = Math.random() * this.app.screen.width;
      asteroidContainer.y = Math.random() * this.app.screen.height;
    } while (Math.hypot(asteroidContainer.x - this.station.x, asteroidContainer.y - this.station.y) < 100);
    
    asteroidContainer.crystals = this.asteroidCapacity;
    asteroidContainer.sprite = asteroidSprite;
    this.asteroids.addChild(asteroidContainer);
    
    // Spawn animation
    this.effects.spawnAnimation(asteroidContainer);
  }

  gameLoop(delta) {
    const elapsedSecs = delta / 60;

    this.drones.children.forEach(drone => {
      switch (drone.state) {
        case 'seeking':
          if (!drone.targetAsteroid) {
            const available = this.asteroids.children.filter(a => a.crystals > 0);
            if (available.length > 0) {
              drone.targetAsteroid = available[Math.floor(Math.random() * available.length)];
            }
          }
          if (drone.targetAsteroid) {
            this.moveDrone(drone, drone.targetAsteroid.x, drone.targetAsteroid.y, elapsedSecs);
            if (this.hasReachedTarget(drone, drone.targetAsteroid)) {
              drone.state = 'mining';
              drone.miningTimer = INITIAL_VALUES.MINING_TIME;
              // Start mining effects
              this.effects.createImpactEffect(this.app.stage, {
                x: drone.x,
                y: drone.y,
                color: 0x00ff00
              });
              this.effects.createSpiralParticles(this.app.stage, {
                x: drone.x,
                y: drone.y
              });
            }
          }
          break;

        case 'mining':
          drone.miningTimer -= elapsedSecs;
          if (drone.miningTimer <= 0) {
            const mineAmount = Math.min(
              this.droneCargo - drone.cargo,
              drone.targetAsteroid.crystals
            );
            drone.cargo += mineAmount;
            drone.targetAsteroid.crystals -= mineAmount;
            
            // Mining complete effects
            this.effects.flashColor(drone.sprite, { color: 0x00ff00 });
            this.effects.showFloatingText(drone, `+${mineAmount}`);
            
            if (drone.targetAsteroid.crystals <= 0) {
              // Asteroid depletion effects
              this.effects.createExplosionParticles(this.app.stage, {
                x: drone.targetAsteroid.x,
                y: drone.targetAsteroid.y
              });
              this.effects.screenShake(this.app.stage);
              
              this.asteroids.removeChild(drone.targetAsteroid);
              this.createAsteroid();
            }
            
            drone.state = 'returning';
          }
          break;

        case 'returning':
          this.moveDrone(drone, this.station.x, this.station.y, elapsedSecs);
          if (this.hasReachedTarget(drone, this.station)) {
            // Crystal transfer effects
            this.effects.createSpiralParticles(this.app.stage, {
              x: this.station.x,
              y: this.station.y,
              color: 0x00ffff
            });
            this.effects.showFloatingText(this.station, `+${drone.cargo}`);
            
            this.crystals += drone.cargo;
            drone.cargo = 0;
            drone.targetAsteroid = null;
            drone.state = 'seeking';
          }
          break;
      }
    });
  }

  moveDrone(drone, targetX, targetY, elapsedSecs) {
    const dx = targetX - drone.x;
    const dy = targetY - drone.y;
    const distance = Math.hypot(dx, dy);
    if (distance > 0) {
      const moveDistance = this.droneSpeed * elapsedSecs;
      const ratio = Math.min(1, moveDistance / distance);
      drone.x += dx * ratio;
      drone.y += dy * ratio;
      drone.rotation = Math.atan2(dy, dx);
      
      // Movement particle trail
      this.effects.createImpactEffect(this.app.stage, {
        x: drone.x,
        y: drone.y,
        radius: 2,
        duration: 0.1,
        alpha: 0.2
      });
    }
  }

  hasReachedTarget(drone, target) {
    return Math.hypot(drone.x - target.x, drone.y - target.y) < 5;
  }

  upgradeDroneCount() {
    if (this.crystals >= this.droneCountCost) {
      this.crystals -= this.droneCountCost;
      this.droneCount++;
      this.createDrone();
      this.droneCountCost *= 2;
      
      // Upgrade effects
      this.effects.screenShake(this.app.stage);
      this.effects.createExplosionParticles(this.app.stage, {
        x: this.station.x,
        y: this.station.y,
        color: 0xffff00
      });
    }
  }

  upgradeDroneSpeed() {
    if (this.crystals >= this.droneSpeedCost) {
      this.crystals -= this.droneSpeedCost;
      this.droneSpeed *= 1.2;
      this.droneSpeedCost *= 2;
      
      // Upgrade effects
      this.drones.children.forEach(drone => {
        this.effects.flashColor(drone.sprite, { color: 0xffff00 });
      });
    }
  }

  upgradeDroneCargo() {
    if (this.crystals >= this.droneCargoCost) {
      this.crystals -= this.droneCargoCost;
      this.droneCargo *= 1.5;
      this.droneCargoCost *= 2;
      
      // Upgrade effects
      this.drones.children.forEach(drone => {
        this.effects.flashColor(drone.sprite, { color: 0xffff00 });
      });
    }
  }

  upgradeAsteroidCapacity() {
    if (this.crystals >= this.asteroidCapacityCost) {
      this.crystals -= this.asteroidCapacityCost;
      this.asteroidCapacity *= 1.5;
      this.asteroidCapacityCost *= 2;
      
      // Upgrade effects
      this.asteroids.children.forEach(asteroid => {
        this.effects.flashColor(asteroid.sprite, { color: 0xffff00 });
      });
    }
  }

  upgradeMaxAsteroids() {
    if (this.crystals >= this.maxAsteroidsCost) {
      this.crystals -= this.maxAsteroidsCost;
      this.maxAsteroids++;
      this.createAsteroid();
      this.maxAsteroidsCost *= 2;
      
      // Upgrade effects
      this.effects.screenShake(this.app.stage);
      this.effects.createExplosionParticles(this.app.stage, {
        x: this.station.x,
        y: this.station.y,
        color: 0xffff00
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
