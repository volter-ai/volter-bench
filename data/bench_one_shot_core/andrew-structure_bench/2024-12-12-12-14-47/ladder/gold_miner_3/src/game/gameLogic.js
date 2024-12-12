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
        this.droneCapacity = INITIAL_VALUES.DRONE_CAPACITY;
        this.maxAsteroids = INITIAL_VALUES.MAX_ASTEROIDS;
        this.asteroidCapacity = INITIAL_VALUES.ASTEROID_CAPACITY;
        
        this.droneCost = UPGRADE_COSTS.DRONE_COUNT;
        this.speedCost = UPGRADE_COSTS.DRONE_SPEED;
        this.capacityCost = UPGRADE_COSTS.DRONE_CAPACITY;
        this.asteroidCountCost = UPGRADE_COSTS.MAX_ASTEROIDS;
        this.asteroidCapacityCost = UPGRADE_COSTS.ASTEROID_CAPACITY;

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

        // Create station container
        this.stationContainer = new PIXI.Container();
        this.station = this.getSprite(SPRITES.station);
        this.station.anchor.set(0.5);
        this.stationContainer.addChild(this.station);
        this.stationContainer.x = SCREEN_SIZE.width / 2;
        this.stationContainer.y = SCREEN_SIZE.height / 2;
        
        // Create containers
        this.drones = new PIXI.Container();
        this.asteroids = new PIXI.Container();

        this.app.stage.addChild(this.stationContainer);
        this.app.stage.addChild(this.asteroids);
        this.app.stage.addChild(this.drones);

        // Station effects
        this.effects.createParticleSystem(this.stationContainer, {
            maxParticles: 20,
            radius: 60,
            spawnInterval: 5
        });

        // Create initial drones and asteroids
        this.createDrone();
        this.createAsteroid();
    }

    createDrone() {
        const container = new PIXI.Container();
        const drone = this.getSprite(SPRITES.drone);
        drone.anchor.set(0.5);
        container.addChild(drone);
        
        // Add shadow
        this.effects.createShadow(container, drone, {
            offsetY: 10
        });
        
        container.x = this.stationContainer.x;
        container.y = this.stationContainer.y;
        container.cargo = 0;
        container.state = 'idle';
        container.target = null;
        container.miningTimer = 0;
        container.sprite = drone;
        
        // Add particle system for trail
        container.particleSystem = this.effects.createParticleSystem(container, {
            maxParticles: 10,
            spawnInterval: 3
        });
        
        this.effects.spawnAnimation(container);
        this.drones.addChild(container);
    }

    createAsteroid() {
        if (this.asteroids.children.length >= this.maxAsteroids) return;

        const container = new PIXI.Container();
        const asteroid = this.getSprite(SPRITES.asteroid);
        asteroid.anchor.set(0.5);
        container.addChild(asteroid);
        
        // Add shadow
        this.effects.createShadow(container, asteroid, {
            offsetY: 15
        });
        
        container.x = Math.random() * SCREEN_SIZE.width;
        container.y = Math.random() * SCREEN_SIZE.height;
        container.crystals = this.asteroidCapacity;
        container.claimed = false;
        container.sprite = asteroid;
        
        this.effects.spawnAnimation(container);
        this.asteroids.addChild(container);
    }

    gameLoop(delta) {
        const elapsedSecs = delta / 60;

        this.drones.children.forEach(drone => {
            switch(drone.state) {
                case 'idle':
                    const freeAsteroid = this.asteroids.children.find(a => !a.claimed && a.crystals > 0);
                    if (freeAsteroid) {
                        drone.target = freeAsteroid;
                        freeAsteroid.claimed = true;
                        drone.state = 'moving_to_asteroid';
                        this.effects.createImpactEffect(freeAsteroid, {
                            color: 0x4a9eff
                        });
                    }
                    break;

                case 'moving_to_asteroid':
                    const toAsteroid = this.moveTo(drone, drone.target.x, drone.target.y, elapsedSecs);
                    if (toAsteroid) {
                        drone.state = 'mining';
                        drone.miningTimer = 0;
                        this.effects.createImpactEffect(drone.target);
                    }
                    break;

                case 'mining':
                    drone.miningTimer += elapsedSecs;
                    
                    // Mining particles
                    if (Math.random() < 0.1) {
                        this.effects.createSpiralParticles(drone.target, {
                            color: 0x4a9eff
                        });
                    }
                    
                    if (drone.miningTimer >= INITIAL_VALUES.MINING_TIME) {
                        const mineAmount = Math.min(
                            this.droneCapacity - drone.cargo,
                            drone.target.crystals
                        );
                        drone.cargo += mineAmount;
                        drone.target.crystals -= mineAmount;
                        
                        this.effects.showFloatingText(drone.target, `+${mineAmount}`);
                        this.effects.flashColor(drone.target.sprite, {
                            color: 0x4a9eff
                        });

                        if (drone.target.crystals <= 0) {
                            this.effects.createExplosionParticles(this.app.stage, {
                                x: drone.target.x,
                                y: drone.target.y
                            });
                            this.asteroids.removeChild(drone.target);
                            this.createAsteroid();
                        }
                        drone.state = 'returning';
                    }
                    break;

                case 'returning':
                    const toStation = this.moveTo(drone, this.stationContainer.x, this.stationContainer.y, elapsedSecs);
                    if (toStation) {
                        this.crystals += drone.cargo;
                        this.effects.createSpiralParticles(this.stationContainer, {
                            count: drone.cargo,
                            color: 0x4a9eff
                        });
                        drone.cargo = 0;
                        drone.target = null;
                        drone.state = 'idle';
                    }
                    break;
            }
        });

        if (this.asteroids.children.length < this.maxAsteroids) {
            this.createAsteroid();
        }
    }

    moveTo(drone, targetX, targetY, elapsedSecs) {
        const dx = targetX - drone.x;
        const dy = targetY - drone.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 5) {
            drone.x = targetX;
            drone.y = targetY;
            return true;
        }

        const moveDistance = this.droneSpeed * elapsedSecs;
        const ratio = moveDistance / distance;
        
        drone.x += dx * ratio;
        drone.y += dy * ratio;
        
        // Smooth rotation
        const targetRotation = Math.atan2(dy, dx);
        const rotationDiff = targetRotation - drone.sprite.rotation;
        drone.sprite.rotation += rotationDiff * 0.1;
        
        return false;
    }

    upgradeDroneCount() {
        if (this.crystals >= this.droneCost) {
            this.crystals -= this.droneCost;
            this.droneCount++;
            this.createDrone();
            this.droneCost *= 2;
            this.effects.screenShake(this.app.stage, { intensity: 5 });
        }
    }

    upgradeDroneSpeed() {
        if (this.crystals >= this.speedCost) {
            this.crystals -= this.speedCost;
            this.droneSpeed *= 1.2;
            this.speedCost *= 2;
            this.drones.children.forEach(drone => {
                this.effects.highlightCharacter(drone.sprite);
            });
        }
    }

    upgradeDroneCapacity() {
        if (this.crystals >= this.capacityCost) {
            this.crystals -= this.capacityCost;
            this.droneCapacity = Math.floor(this.droneCapacity * 1.5);
            this.capacityCost *= 2;
            this.effects.screenShake(this.app.stage, { intensity: 3 });
        }
    }

    upgradeMaxAsteroids() {
        if (this.crystals >= this.asteroidCountCost) {
            this.crystals -= this.asteroidCountCost;
            this.maxAsteroids++;
            this.createAsteroid();
            this.asteroidCountCost *= 2;
            this.effects.screenShake(this.app.stage, { intensity: 4 });
        }
    }

    upgradeAsteroidCapacity() {
        if (this.crystals >= this.asteroidCapacityCost) {
            this.crystals -= this.asteroidCapacityCost;
            this.asteroidCapacity = Math.floor(this.asteroidCapacity * 1.5);
            this.asteroidCapacityCost *= 2;
            this.asteroids.children.forEach(asteroid => {
                this.effects.highlightCharacter(asteroid.sprite);
            });
        }
    }

    destroy() {
        this.effects.destroyAll();
        this.app.destroy(true);
    }
}
