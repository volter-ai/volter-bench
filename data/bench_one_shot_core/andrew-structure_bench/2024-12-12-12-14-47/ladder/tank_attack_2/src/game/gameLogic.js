import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, SPAWN_POSITIONS } from './gameData';
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
    
    // Create effects library
    this.effects = new EffectsLibrary(this.app);

    this.ready = false;
    this.credits = 0;
    this.tankHealth = INITIAL_VALUES.TANK_HEALTH;
    this.tankDamage = INITIAL_VALUES.TANK_DAMAGE;
    this.tankSpeed = INITIAL_VALUES.TANK_SPEED;
    this.tankCount = INITIAL_VALUES.TANK_COUNT;
    this.baseReward = INITIAL_VALUES.BASE_REWARD;
    
    this.tankHealthCost = UPGRADE_COSTS.TANK_HEALTH;
    this.tankDamageCost = UPGRADE_COSTS.TANK_DAMAGE;
    this.tankSpeedCost = UPGRADE_COSTS.TANK_SPEED;
    this.tankCountCost = UPGRADE_COSTS.TANK_COUNT;
    this.baseRewardCost = UPGRADE_COSTS.BASE_REWARD;

    this.tankSpawnTimer = 0;
    this.baseSpawnTimer = 0;

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(key) {
    const sprite = new PIXI.Sprite(PIXI.Loader.shared.resources[key].texture);
    sprite.width = SPRITES[key].width;
    sprite.height = SPRITES[key].height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite('background');
    this.tanks = new PIXI.Container();
    this.bases = new PIXI.Container();
    
    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.tanks);
    this.app.stage.addChild(this.bases);

    // Create initial tanks and bases
    this.spawnTank();
    SPAWN_POSITIONS.BASES.forEach(pos => this.spawnBase(pos.x, pos.y));
  }

  spawnTank() {
    if (this.tanks.children.length >= this.tankCount) return;
    
    const pos = SPAWN_POSITIONS.TANKS[this.tanks.children.length % SPAWN_POSITIONS.TANKS.length];
    
    // Create container for tank
    const tankContainer = new PIXI.Container();
    const tankSprite = this.getSprite('tank');
    tankSprite.anchor.set(0.5);
    tankContainer.addChild(tankSprite);
    
    // Create shadow
    this.effects.createShadow(tankContainer, tankSprite);
    
    // Position container
    tankContainer.x = pos.x;
    tankContainer.y = pos.y;
    tankContainer.sprite = tankSprite;
    tankContainer.health = this.tankHealth;
    tankContainer.maxHealth = this.tankHealth;
    
    this.tanks.addChild(tankContainer);
    
    // Spawn effects
    this.effects.spawnAnimation(tankContainer);
    this.effects.createParticleSystem(tankContainer, {
      maxParticles: 20,
      radius: 30
    });
  }

  spawnBase(x, y) {
    const baseContainer = new PIXI.Container();
    const baseSprite = this.getSprite('base');
    baseSprite.anchor.set(0.5);
    baseContainer.addChild(baseSprite);
    
    // Create shadow
    this.effects.createShadow(baseContainer, baseSprite);
    
    baseContainer.x = x;
    baseContainer.y = y;
    baseContainer.sprite = baseSprite;
    baseContainer.health = INITIAL_VALUES.BASE_HEALTH;
    baseContainer.maxHealth = INITIAL_VALUES.BASE_HEALTH;
    
    this.bases.addChild(baseContainer);
    
    // Spawn effects
    this.effects.spawnAnimation(baseContainer);
  }

  gameLoop(delta) {
    const elapsedSecs = delta / 60;

    // Spawn timers
    this.tankSpawnTimer += elapsedSecs;
    if (this.tankSpawnTimer >= INITIAL_VALUES.TANK_SPAWN_TIME) {
      this.spawnTank();
      this.tankSpawnTimer = 0;
    }

    this.baseSpawnTimer += elapsedSecs;
    if (this.baseSpawnTimer >= INITIAL_VALUES.BASE_SPAWN_TIME && this.bases.children.length < SPAWN_POSITIONS.BASES.length) {
      const pos = SPAWN_POSITIONS.BASES[this.bases.children.length];
      this.spawnBase(pos.x, pos.y);
      this.baseSpawnTimer = 0;
    }

    // Tank movement and combat
    this.tanks.children.forEach(tank => {
      if (this.bases.children.length === 0) return;

      // Find nearest base
      let nearestBase = this.bases.children[0];
      let nearestDist = this.getDistance(tank, nearestBase);

      this.bases.children.forEach(base => {
        const dist = this.getDistance(tank, base);
        if (dist < nearestDist) {
          nearestDist = dist;
          nearestBase = base;
        }
      });

      // Move toward nearest base
      if (nearestDist > 50) {
        const angle = Math.atan2(nearestBase.y - tank.y, nearestBase.x - tank.x);
        tank.x += Math.cos(angle) * this.tankSpeed * elapsedSecs;
        tank.y += Math.sin(angle) * this.tankSpeed * elapsedSecs;
        
        // Create movement particles
        if (Math.random() < 0.1) {
          this.effects.createSpiralParticles(this.app.stage, {
            x: tank.x - Math.cos(angle) * 20,
            y: tank.y - Math.sin(angle) * 20,
            count: 5
          });
        }
      } else {
        // Attack base
        nearestBase.health -= this.tankDamage * elapsedSecs;
        tank.health -= INITIAL_VALUES.BASE_DAMAGE * elapsedSecs;
        
        // Combat effects
        if (Math.random() < 0.1) {
          this.effects.createImpactEffect(this.app.stage, {
            x: tank.x + (Math.random() - 0.5) * 20,
            y: tank.y + (Math.random() - 0.5) * 20
          });
          
          this.effects.flashColor(tank.sprite, { color: 0xFF0000 });
          this.effects.flashColor(nearestBase.sprite, { color: 0xFF0000 });
          
          this.effects.showFloatingText(tank, `-${Math.floor(INITIAL_VALUES.BASE_DAMAGE)}`, {
            color: 0xFF0000
          });
        }

        // Check tank death
        if (tank.health <= 0) {
          this.effects.createExplosionParticles(this.app.stage, {
            x: tank.x,
            y: tank.y,
            count: 30
          });
          this.effects.screenShake(this.app.stage, { intensity: 5 });
          this.tanks.removeChild(tank);
        }

        // Check base destruction
        if (nearestBase.health <= 0) {
          this.credits += this.baseReward;
          this.effects.createExplosionParticles(this.app.stage, {
            x: nearestBase.x,
            y: nearestBase.y,
            count: 50,
            color: 0xFFD700
          });
          this.effects.screenShake(this.app.stage, { intensity: 10 });
          this.effects.showFloatingText(nearestBase, `+${Math.floor(this.baseReward)}`, {
            color: 0xFFD700
          });
          this.bases.removeChild(nearestBase);
        }
      }
    });
  }

  getDistance(obj1, obj2) {
    const dx = obj1.x - obj2.x;
    const dy = obj1.y - obj2.y;
    return Math.sqrt(dx * dx + dy * dy);
  }

  upgradeTankHealth() {
    if (this.credits >= this.tankHealthCost) {
      this.credits -= this.tankHealthCost;
      this.tankHealth *= 1.2;
      this.tankHealthCost *= 2;
      this.tanks.children.forEach(tank => {
        this.effects.highlightCharacter(tank.sprite);
        this.effects.createSpiralParticles(this.app.stage, {
          x: tank.x,
          y: tank.y,
          color: 0x00FF00
        });
      });
    }
  }

  upgradeTankDamage() {
    if (this.credits >= this.tankDamageCost) {
      this.credits -= this.tankDamageCost;
      this.tankDamage *= 1.2;
      this.tankDamageCost *= 2;
      this.tanks.children.forEach(tank => {
        this.effects.highlightCharacter(tank.sprite);
        this.effects.createSpiralParticles(this.app.stage, {
          x: tank.x,
          y: tank.y,
          color: 0xFF0000
        });
      });
    }
  }

  upgradeTankSpeed() {
    if (this.credits >= this.tankSpeedCost) {
      this.credits -= this.tankSpeedCost;
      this.tankSpeed *= 1.2;
      this.tankSpeedCost *= 2;
      this.tanks.children.forEach(tank => {
        this.effects.highlightCharacter(tank.sprite);
        this.effects.createSpiralParticles(this.app.stage, {
          x: tank.x,
          y: tank.y,
          color: 0x00FFFF
        });
      });
    }
  }

  upgradeTankCount() {
    if (this.credits >= this.tankCountCost) {
      this.credits -= this.tankCountCost;
      this.tankCount += 1;
      this.tankCountCost *= 2;
      this.spawnTank();
    }
  }

  upgradeBaseReward() {
    if (this.credits >= this.baseRewardCost) {
      this.credits -= this.baseRewardCost;
      this.baseReward *= 1.2;
      this.baseRewardCost *= 2;
      this.bases.children.forEach(base => {
        this.effects.highlightCharacter(base.sprite);
        this.effects.createSpiralParticles(this.app.stage, {
          x: base.x,
          y: base.y,
          color: 0xFFD700
        });
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
