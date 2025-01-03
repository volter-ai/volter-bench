import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, BATTLE_POSITIONS } from './gameData';
import { SPRITES } from './assetManifest';
import { loadAssets } from './utils'

const SCREEN_SIZE = {
  width: 800,
  height: 600
}

export class GameLogic {
  constructor(container) {
    // Define all methods that will be used in callbacks first
    this.createGameObjects = () => {
      this.background = this.getSprite(SPRITES.background);
      this.friendlyTanks = new PIXI.Container();
      this.enemyTanks = new PIXI.Container();
      this.projectiles = new PIXI.Container();

      this.app.stage.addChild(this.background);
      this.app.stage.addChild(this.friendlyTanks);
      this.app.stage.addChild(this.enemyTanks);
      this.app.stage.addChild(this.projectiles);

      // Initial spawn
      this.spawnInitialTanks();
    };

    this.gameLoop = (delta) => {
      const currentTime = performance.now();
      const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
      this.lastTimestamp = currentTime;

      this.moveTanks(elapsedSecs);
      this.updateCombat(elapsedSecs);
      this.moveProjectiles(elapsedSecs);
      this.checkProjectileCollisions();
    };

    // Initialize the application
    this.app = new PIXI.Application({
      width: SCREEN_SIZE.width,
      height: SCREEN_SIZE.height,
      backgroundColor: 0x222C37,
    });

    container.appendChild(this.app.view);

    this.ready = false;
    this.credits = 0;
    this.lastTimestamp = performance.now();

    // Game attributes
    this.tankCount = INITIAL_VALUES.TANK_COUNT;
    this.tankDamage = INITIAL_VALUES.TANK_DAMAGE;
    this.fireRate = INITIAL_VALUES.FIRE_RATE;
    this.tankHealth = INITIAL_VALUES.TANK_HEALTH;
    this.tankRange = INITIAL_VALUES.TANK_RANGE;

    // Upgrade costs
    this.tankCountCost = UPGRADE_COSTS.TANK_COUNT;
    this.tankDamageCost = UPGRADE_COSTS.TANK_DAMAGE;
    this.fireRateCost = UPGRADE_COSTS.FIRE_RATE;
    this.tankHealthCost = UPGRADE_COSTS.TANK_HEALTH;
    this.tankRangeCost = UPGRADE_COSTS.TANK_RANGE;

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop);
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

  spawnInitialTanks() {
    for (let i = 0; i < this.tankCount; i++) {
      this.spawnFriendlyTank(i);
    }
    for (let i = 0; i < INITIAL_VALUES.ENEMY_COUNT; i++) {
      this.spawnEnemyTank(i);
    }
  }

  spawnFriendlyTank(position) {
    const tank = this.getSprite(SPRITES.friendlyTank);
    tank.anchor.set(0.5);
    tank.x = 0;
    tank.y = SCREEN_SIZE.height / 2;
    tank.targetX = BATTLE_POSITIONS.FRIENDLY[position % BATTLE_POSITIONS.FRIENDLY.length].x;
    tank.targetY = BATTLE_POSITIONS.FRIENDLY[position % BATTLE_POSITIONS.FRIENDLY.length].y;
    tank.health = this.tankHealth;
    tank.fireTimer = 0;
    this.friendlyTanks.addChild(tank);
  }

  spawnEnemyTank(position) {
    const tank = this.getSprite(SPRITES.enemyTank);
    tank.anchor.set(0.5);
    tank.x = SCREEN_SIZE.width;
    tank.y = SCREEN_SIZE.height / 2;
    tank.targetX = BATTLE_POSITIONS.ENEMY[position % BATTLE_POSITIONS.ENEMY.length].x;
    tank.targetY = BATTLE_POSITIONS.ENEMY[position % BATTLE_POSITIONS.ENEMY.length].y;
    tank.health = INITIAL_VALUES.TANK_HEALTH;
    tank.fireTimer = 0;
    this.enemyTanks.addChild(tank);
  }

  moveTanks(elapsedSecs) {
    const moveToTarget = (tank) => {
      const dx = tank.targetX - tank.x;
      const dy = tank.targetY - tank.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance > 1) {
        tank.x += (dx / distance) * INITIAL_VALUES.TANK_SPEED * elapsedSecs;
        tank.y += (dy / distance) * INITIAL_VALUES.TANK_SPEED * elapsedSecs;
      }
    };

    this.friendlyTanks.children.forEach(moveToTarget);
    this.enemyTanks.children.forEach(moveToTarget);
  }

  updateCombat(elapsedSecs) {
    this.friendlyTanks.children.forEach(tank => {
      tank.fireTimer += elapsedSecs;
      if (tank.fireTimer >= 1 / this.fireRate) {
        this.fireAtNearestEnemy(tank, true);
        tank.fireTimer = 0;
      }
    });

    this.enemyTanks.children.forEach(tank => {
      tank.fireTimer += elapsedSecs;
      if (tank.fireTimer >= 1 / INITIAL_VALUES.FIRE_RATE) {
        this.fireAtNearestEnemy(tank, false);
        tank.fireTimer = 0;
      }
    });
  }

  fireAtNearestEnemy(tank, isFriendly) {
    const targets = isFriendly ? this.enemyTanks.children : this.friendlyTanks.children;
    let nearest = null;
    let minDistance = Infinity;

    targets.forEach(target => {
      const distance = Math.sqrt(
        Math.pow(target.x - tank.x, 2) + 
        Math.pow(target.y - tank.y, 2)
      );
      if (distance < minDistance) {
        minDistance = distance;
        nearest = target;
      }
    });

    if (nearest && minDistance <= (isFriendly ? this.tankRange : INITIAL_VALUES.TANK_RANGE)) {
      this.createProjectile(tank, nearest, isFriendly);
    }
  }

  createProjectile(source, target, isFriendly) {
    const projectile = this.getSprite(SPRITES.projectile);
    projectile.anchor.set(0.5);
    projectile.tint = isFriendly ? 0x00ff00 : 0xff0000;
    projectile.x = source.x;
    projectile.y = source.y;
    
    const angle = Math.atan2(target.y - source.y, target.x - source.x);
    projectile.dx = Math.cos(angle) * INITIAL_VALUES.PROJECTILE_SPEED;
    projectile.dy = Math.sin(angle) * INITIAL_VALUES.PROJECTILE_SPEED;
    projectile.isFriendly = isFriendly;
    projectile.damage = isFriendly ? this.tankDamage : INITIAL_VALUES.TANK_DAMAGE;
    
    this.projectiles.addChild(projectile);
  }

  moveProjectiles(elapsedSecs) {
    this.projectiles.children.forEach(projectile => {
      projectile.x += projectile.dx * elapsedSecs;
      projectile.y += projectile.dy * elapsedSecs;

      if (projectile.x < 0 || projectile.x > SCREEN_SIZE.width ||
          projectile.y < 0 || projectile.y > SCREEN_SIZE.height) {
        this.projectiles.removeChild(projectile);
      }
    });
  }

  checkProjectileCollisions() {
    const projectilesToRemove = new Set();
    
    this.projectiles.children.forEach(projectile => {
      if (projectilesToRemove.has(projectile)) return;
      
      const targets = projectile.isFriendly ? this.enemyTanks : this.friendlyTanks;
      
      targets.children.forEach(tank => {
        const dx = projectile.x - tank.x;
        const dy = projectile.y - tank.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < INITIAL_VALUES.COLLISION_RADIUS) {
          tank.health -= projectile.damage;
          projectilesToRemove.add(projectile);

          if (tank.health <= 0) {
            targets.removeChild(tank);
            if (!projectile.isFriendly) {
              this.spawnFriendlyTank(this.friendlyTanks.children.length);
            } else {
              this.credits += INITIAL_VALUES.CREDITS_PER_KILL;
              this.spawnEnemyTank(this.enemyTanks.children.length);
            }
          }
        }
      });
    });
    
    projectilesToRemove.forEach(projectile => {
      if (this.projectiles.children.includes(projectile)) {
        this.projectiles.removeChild(projectile);
      }
    });
  }

  upgradeTankCount() {
    if (this.credits >= this.tankCountCost) {
      this.credits -= this.tankCountCost;
      this.tankCount++;
      this.spawnFriendlyTank(this.friendlyTanks.children.length);
      this.tankCountCost *= 2;
    }
  }

  upgradeTankDamage() {
    if (this.credits >= this.tankDamageCost) {
      this.credits -= this.tankDamageCost;
      this.tankDamage *= 1.2;
      this.tankDamageCost *= 2;
    }
  }

  upgradeFireRate() {
    if (this.credits >= this.fireRateCost) {
      this.credits -= this.fireRateCost;
      this.fireRate *= 1.2;
      this.fireRateCost *= 2;
    }
  }

  upgradeTankHealth() {
    if (this.credits >= this.tankHealthCost) {
      this.credits -= this.tankHealthCost;
      this.tankHealth *= 1.2;
      this.tankHealthCost *= 2;
    }
  }

  upgradeTankRange() {
    if (this.credits >= this.tankRangeCost) {
      this.credits -= this.tankRangeCost;
      this.tankRange *= 1.2;
      this.tankRangeCost *= 2;
    }
  }

  destroy() {
    this.app.destroy(true);
  }
}
