import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, GAMEPLAY } from './gameData';
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
      backgroundColor: 0x222C37,
    });

    container.appendChild(this.app.view);
    
    // Initialize effects library
    this.effects = new EffectsLibrary(this.app);

    this.ready = false;
    this.credits = 0;
    this.tankSpeed = INITIAL_VALUES.TANK_SPEED;
    this.tankHealth = INITIAL_VALUES.TANK_HEALTH;
    this.tankDamage = INITIAL_VALUES.TANK_DAMAGE;
    this.tankFireRate = INITIAL_VALUES.TANK_FIRE_RATE;
    this.tankRange = INITIAL_VALUES.TANK_RANGE;
    this.tankCount = INITIAL_VALUES.TANK_COUNT;

    this.costs = {...UPGRADE_COSTS};
    
    this.enemySpawnTimer = 0;
    this.lastTimestamp = performance.now();

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop);
      this.ready = true;
    });
  }

  getSprite = (spriteConfig) => {
    const texture = PIXI.Texture.from(spriteConfig.path);
    const sprite = new PIXI.Sprite(texture);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    return sprite;
  }

  createGameObjects = () => {
    this.background = this.getSprite(SPRITES.background);
    this.tanks = new PIXI.Container();
    this.enemies = new PIXI.Container();
    this.bullets = new PIXI.Container();
    this.healthBars = new PIXI.Container();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.tanks);
    this.app.stage.addChild(this.enemies);
    this.app.stage.addChild(this.bullets);
    this.app.stage.addChild(this.healthBars);

    for (let i = 0; i < this.tankCount; i++) {
      this.createTank();
    }
  }

  createTank = () => {
    const container = new PIXI.Container();
    const tank = this.getSprite(SPRITES.friendlyTank);
    tank.anchor.set(0.5);
    
    // Create shadow
    this.effects.createShadow(container, tank, {
      offsetY: 10
    });
    
    container.addChild(tank);
    container.x = SCREEN_SIZE.width / 2;
    container.y = SCREEN_SIZE.height / 2;
    container.health = this.tankHealth;
    container.fireTimer = 0;
    container.sprite = tank; // Reference to sprite for effects
    
    this.tanks.addChild(container);
    this.createHealthBar(container);

    // Spawn animation
    this.effects.spawnAnimation(container, {
      duration: 0.5
    });
    
    // Create particle system for tank
    const particleSystem = this.effects.createParticleSystem(container, {
      maxParticles: 20,
      radius: 30
    });
    
    // Add idle animation
    this.effects.idleAnimation(container, {
      duration: 2
    });

    return container;
  }

  createEnemy = () => {
    const container = new PIXI.Container();
    const enemy = this.getSprite(SPRITES.enemyTank);
    enemy.anchor.set(0.5);
    
    // Create shadow
    this.effects.createShadow(container, enemy, {
      offsetY: 10
    });
    
    container.addChild(enemy);
    container.sprite = enemy;
    
    const side = Math.floor(Math.random() * 4);
    switch(side) {
      case 0:
        container.x = Math.random() * SCREEN_SIZE.width;
        container.y = -32;
        break;
      case 1:
        container.x = SCREEN_SIZE.width + 32;
        container.y = Math.random() * SCREEN_SIZE.height;
        break;
      case 2:
        container.x = Math.random() * SCREEN_SIZE.width;
        container.y = SCREEN_SIZE.height + 32;
        break;
      case 3:
        container.x = -32;
        container.y = Math.random() * SCREEN_SIZE.height;
        break;
    }
    
    container.health = GAMEPLAY.ENEMY_HEALTH;
    this.enemies.addChild(container);
    this.createHealthBar(container);

    // Spawn animation
    this.effects.spawnAnimation(container, {
      duration: 0.3
    });

    return container;
  }

  createHealthBar = (entity) => {
    const bar = new PIXI.Graphics();
    bar.beginFill(0x00ff00);
    bar.drawRect(-25, -40, 50, 5);
    bar.endFill();
    bar.owner = entity;
    this.healthBars.addChild(bar);
  }

  createBullet = (shooter, target) => {
    const container = new PIXI.Container();
    const bullet = new PIXI.Graphics();
    bullet.beginFill(0xffff00);
    bullet.drawCircle(0, 0, 3);
    bullet.endFill();
    container.addChild(bullet);
    
    container.x = shooter.x;
    container.y = shooter.y;
    
    const angle = Math.atan2(target.y - shooter.y, target.x - shooter.x);
    container.rotation = angle;
    container.dx = Math.cos(angle) * GAMEPLAY.BULLET_SPEED;
    container.dy = Math.sin(angle) * GAMEPLAY.BULLET_SPEED;
    container.damage = shooter.parent === this.tanks ? this.tankDamage : GAMEPLAY.ENEMY_DAMAGE;
    
    this.bullets.addChild(container);

    // Muzzle flash effect
    this.effects.createImpactEffect(shooter, {
      radius: 15,
      duration: 0.1,
      alpha: 0.3
    });

    // Recoil animation
    this.effects.lungeAnimation(shooter, {
      x: shooter.x - Math.cos(angle) * 10,
      y: shooter.y - Math.sin(angle) * 10
    });
  }

  gameLoop = (delta) => {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.enemySpawnTimer += elapsedSecs;
    if (this.enemySpawnTimer >= INITIAL_VALUES.ENEMY_SPAWN_RATE) {
      this.createEnemy();
      this.enemySpawnTimer = 0;
    }

    this.updateTanks(elapsedSecs);
    this.updateEnemies(elapsedSecs);
    this.updateBullets(elapsedSecs);
    this.updateHealthBars();
  }

  updateTanks = (elapsedSecs) => {
    this.tanks.children.forEach(tank => {
      const target = this.findNearestEnemy(tank);
      if (target) {
        const dx = target.x - tank.x;
        const dy = target.y - tank.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        tank.rotation = Math.atan2(dy, dx);

        if (distance > this.tankRange) {
          tank.x += (dx / distance) * this.tankSpeed * elapsedSecs;
          tank.y += (dy / distance) * this.tankSpeed * elapsedSecs;
        }

        tank.fireTimer += elapsedSecs;
        if (tank.fireTimer >= 1 / this.tankFireRate) {
          this.createBullet(tank, target);
          tank.fireTimer = 0;
        }
      }
    });
  }

  updateEnemies = (elapsedSecs) => {
    this.enemies.children.forEach(enemy => {
      const dx = SCREEN_SIZE.width/2 - enemy.x;
      const dy = SCREEN_SIZE.height/2 - enemy.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      enemy.rotation = Math.atan2(dy, dx);

      enemy.x += (dx / distance) * GAMEPLAY.ENEMY_SPEED * elapsedSecs;
      enemy.y += (dy / distance) * GAMEPLAY.ENEMY_SPEED * elapsedSecs;
    });
  }

  updateBullets = (elapsedSecs) => {
    this.bullets.children.forEach(bullet => {
      bullet.x += bullet.dx * elapsedSecs;
      bullet.y += bullet.dy * elapsedSecs;

      if (bullet.x < 0 || bullet.x > SCREEN_SIZE.width || 
          bullet.y < 0 || bullet.y > SCREEN_SIZE.height) {
        this.bullets.removeChild(bullet);
        return;
      }

      const targets = bullet.damage === this.tankDamage ? this.enemies : this.tanks;
      targets.children.forEach(target => {
        if (this.checkCollision(bullet, target)) {
          target.health -= bullet.damage;
          
          // Impact effects
          this.effects.createImpactEffect(target, {
            radius: 25,
            duration: 0.2
          });
          this.effects.flashColor(target.sprite, {
            color: 0xFF0000,
            duration: 0.1
          });
          this.effects.showFloatingText(target, `-${bullet.damage}`, {
            color: 0xFF0000
          });
          
          this.bullets.removeChild(bullet);
          
          if (target.health <= 0) {
            if (targets === this.enemies) {
              this.credits += INITIAL_VALUES.CREDITS_PER_KILL;
            }
            // Death effects
            this.effects.createExplosionParticles(this.app.stage, {
              x: target.x,
              y: target.y,
              count: 30
            });
            this.effects.screenShake(this.app.stage, {
              intensity: 5,
              duration: 0.2
            });
            this.removeEntity(target);
          }
        }
      });
    });
  }

  updateHealthBars = () => {
    this.healthBars.children.forEach(bar => {
      if (!bar.owner.parent) {
        this.healthBars.removeChild(bar);
        return;
      }
      bar.x = bar.owner.x;
      bar.y = bar.owner.y;
      bar.scale.x = bar.owner.health / (bar.owner.parent === this.tanks ? this.tankHealth : GAMEPLAY.ENEMY_HEALTH);
    });
  }

  findNearestEnemy = (tank) => {
    let nearest = null;
    let minDistance = Infinity;
    
    this.enemies.children.forEach(enemy => {
      const dx = enemy.x - tank.x;
      const dy = enemy.y - tank.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < minDistance) {
        minDistance = distance;
        nearest = enemy;
      }
    });
    
    return nearest;
  }

  checkCollision = (obj1, obj2) => {
    const dx = obj1.x - obj2.x;
    const dy = obj1.y - obj2.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    return distance < (obj1.width + obj2.width) / 4;
  }

  removeEntity = (entity) => {
    entity.parent.removeChild(entity);
  }

  upgradeTankSpeed = () => {
    if (this.credits >= this.costs.TANK_SPEED) {
      this.credits -= this.costs.TANK_SPEED;
      this.tankSpeed *= 1.1;
      this.costs.TANK_SPEED *= 2;
      this.tanks.children.forEach(tank => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: tank.x,
          y: tank.y
        });
        this.effects.highlightCharacter(tank.sprite);
      });
    }
  }

  upgradeTankHealth = () => {
    if (this.credits >= this.costs.TANK_HEALTH) {
      this.credits -= this.costs.TANK_HEALTH;
      this.tankHealth *= 1.2;
      this.costs.TANK_HEALTH *= 2;
      this.tanks.children.forEach(tank => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: tank.x,
          y: tank.y,
          color: 0x00FF00
        });
        this.effects.highlightCharacter(tank.sprite, {
          color: 0x00FF00
        });
      });
    }
  }

  upgradeTankDamage = () => {
    if (this.credits >= this.costs.TANK_DAMAGE) {
      this.credits -= this.costs.TANK_DAMAGE;
      this.tankDamage *= 1.2;
      this.costs.TANK_DAMAGE *= 2;
      this.tanks.children.forEach(tank => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: tank.x,
          y: tank.y,
          color: 0xFF0000
        });
        this.effects.highlightCharacter(tank.sprite, {
          color: 0xFF0000
        });
      });
    }
  }

  upgradeFireRate = () => {
    if (this.credits >= this.costs.TANK_FIRE_RATE) {
      this.credits -= this.costs.TANK_FIRE_RATE;
      this.tankFireRate *= 1.1;
      this.costs.TANK_FIRE_RATE *= 2;
      this.tanks.children.forEach(tank => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: tank.x,
          y: tank.y,
          color: 0xFFFF00
        });
        this.effects.highlightCharacter(tank.sprite, {
          color: 0xFFFF00
        });
      });
    }
  }

  upgradeRange = () => {
    if (this.credits >= this.costs.TANK_RANGE) {
      this.credits -= this.costs.TANK_RANGE;
      this.tankRange *= 1.1;
      this.costs.TANK_RANGE *= 2;
      this.tanks.children.forEach(tank => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: tank.x,
          y: tank.y,
          color: 0x00FFFF
        });
        this.effects.highlightCharacter(tank.sprite, {
          color: 0x00FFFF
        });
      });
    }
  }

  upgradeTankCount = () => {
    if (this.credits >= this.costs.TANK_COUNT) {
      this.credits -= this.costs.TANK_COUNT;
      this.tankCount++;
      this.createTank();
      this.costs.TANK_COUNT *= 2;
    }
  }

  destroy = () => {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
