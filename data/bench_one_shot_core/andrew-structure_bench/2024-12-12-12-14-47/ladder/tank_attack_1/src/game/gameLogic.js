import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, GAMEPLAY_CONSTANTS } from './gameData';
import { SPRITES } from './assetManifest';

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

    this.ready = false;
    this.coins = 0;
    this.tankDamage = INITIAL_VALUES.TANK_DAMAGE;
    this.tankSpeed = INITIAL_VALUES.TANK_SPEED;
    this.tankFireRate = INITIAL_VALUES.TANK_FIRE_RATE;
    this.maxTanks = INITIAL_VALUES.MAX_TANKS;
    this.multiShot = INITIAL_VALUES.MULTI_SHOT;
    this.baseCoinValue = INITIAL_VALUES.BASE_COIN_VALUE;
    
    this.tankSpawnTimer = 0;
    this.lastTimestamp = performance.now();

    this.upgradeCosts = {...UPGRADE_COSTS};

    // Initialize containers early
    this.tanks = new PIXI.Container();
    this.bases = new PIXI.Container();
    this.projectiles = new PIXI.Container();
    this.effects = new PIXI.Container();

    // Load assets using PIXI loader
    const loader = PIXI.Loader.shared;
    Object.entries(SPRITES).forEach(([key, sprite]) => {
      loader.add(key, sprite.path);
    });

    loader.load(() => {
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  canAffordUpgrade(cost) {
    return this.coins >= cost;
  }

  getSprite(spriteConfig) {
    const texture = PIXI.Loader.shared.resources[spriteConfig].texture;
    if (!texture) {
      console.error('Texture not found for:', spriteConfig);
      return null;
    }
    const sprite = new PIXI.Sprite(texture);
    sprite.width = SPRITES[spriteConfig].width;
    sprite.height = SPRITES[spriteConfig].height;
    return sprite;
  }

  createGameObjects() {
    const background = this.getSprite('background');
    if (background) {
      this.background = background;
      this.app.stage.addChild(this.background);
    }

    this.app.stage.addChild(this.tanks);
    this.app.stage.addChild(this.bases);
    this.app.stage.addChild(this.projectiles);
    this.app.stage.addChild(this.effects);

    this.spawnBase();
  }

  createTank() {
    if (this.tanks.children.length >= this.maxTanks) return;
    
    const tank = this.getSprite('tank');
    if (!tank) return;
    
    tank.anchor.set(0.5);
    tank.x = 50;
    tank.y = Math.random() * (this.app.screen.height - 100) + 50;
    tank.fireTimer = 0;
    this.tanks.addChild(tank);
  }

  spawnBase() {
    const base = this.getSprite('base');
    if (!base) return;
    
    base.anchor.set(0.5);
    base.x = this.app.screen.width - 50;
    base.y = Math.random() * (this.app.screen.height - 100) + 50;
    base.health = INITIAL_VALUES.BASE_HEALTH;
    base.maxHealth = INITIAL_VALUES.BASE_HEALTH;

    const healthBar = new PIXI.Graphics();
    base.healthBar = healthBar;
    healthBar.y = -40;
    base.addChild(healthBar);
    this.updateHealthBar(base);

    this.bases.addChild(base);
  }

  createProjectile(tank, target) {
    const projectile = new PIXI.Graphics();
    projectile.beginFill(0xff0000);
    projectile.drawCircle(0, 0, 4);
    projectile.endFill();
    projectile.x = tank.x;
    projectile.y = tank.y;
    
    const angle = Math.atan2(target.y - tank.y, target.x - tank.x);
    projectile.dx = Math.cos(angle) * GAMEPLAY_CONSTANTS.PROJECTILE_SPEED;
    projectile.dy = Math.sin(angle) * GAMEPLAY_CONSTANTS.PROJECTILE_SPEED;
    projectile.damage = this.tankDamage;
    projectile.hitBases = new Set(); // Track which bases this projectile has hit
    
    this.projectiles.addChild(projectile);
  }

  updateHealthBar(base) {
    const healthBar = base.healthBar;
    healthBar.clear();
    healthBar.beginFill(0xff0000);
    healthBar.drawRect(-30, 0, 60, 5);
    healthBar.beginFill(0x00ff00);
    healthBar.drawRect(-30, 0, (base.health / base.maxHealth) * 60, 5);
    healthBar.endFill();
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.tankSpawnTimer += elapsedSecs;
    if (this.tankSpawnTimer >= INITIAL_VALUES.TANK_SPAWN_RATE) {
      this.createTank();
      this.tankSpawnTimer = 0;
    }

    // Update tanks
    this.tanks.children.forEach(tank => {
      const nearestBase = this.bases.children[0];
      if (!nearestBase) return;

      const dx = nearestBase.x - tank.x;
      const dy = nearestBase.y - tank.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance > INITIAL_VALUES.FIRING_RANGE) {
        tank.x += (this.tankSpeed * elapsedSecs * dx) / distance;
        tank.y += (this.tankSpeed * elapsedSecs * dy) / distance;
      } else {
        tank.fireTimer += elapsedSecs;
        if (tank.fireTimer >= 1 / this.tankFireRate) {
          this.createProjectile(tank, nearestBase);
          tank.fireTimer = 0;
        }
      }
    });

    // Update projectiles
    this.projectiles.children.forEach(projectile => {
      projectile.x += projectile.dx * elapsedSecs;
      projectile.y += projectile.dy * elapsedSecs;

      // Check collisions with bases
      this.bases.children.forEach(base => {
        if (projectile.hitBases.has(base)) return; // Skip if already hit this base

        const dx = projectile.x - base.x;
        const dy = projectile.y - base.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 32) {
          projectile.hitBases.add(base);
          base.health -= projectile.damage;
          this.updateHealthBar(base);

          if (base.health <= 0) {
            this.coins += this.baseCoinValue;
            this.bases.removeChild(base);
            setTimeout(() => this.spawnBase(), INITIAL_VALUES.BASE_SPAWN_DELAY * 1000);
          }

          // Remove projectile if it has hit maximum number of bases
          if (projectile.hitBases.size >= this.multiShot) {
            this.projectiles.removeChild(projectile);
          }
        }
      });

      // Remove projectile if it's off screen
      if (projectile.x < 0 || projectile.x > this.app.screen.width ||
          projectile.y < 0 || projectile.y > this.app.screen.height) {
        this.projectiles.removeChild(projectile);
      }
    });
  }

  upgradeTankDamage() {
    if (!this.canAffordUpgrade(this.upgradeCosts.TANK_DAMAGE)) {
      return false;
    }
    this.coins -= this.upgradeCosts.TANK_DAMAGE;
    this.tankDamage *= 1.2;
    this.upgradeCosts.TANK_DAMAGE *= 2;
    return true;
  }

  upgradeTankSpeed() {
    if (!this.canAffordUpgrade(this.upgradeCosts.TANK_SPEED)) {
      return false;
    }
    this.coins -= this.upgradeCosts.TANK_SPEED;
    this.tankSpeed *= 1.2;
    this.upgradeCosts.TANK_SPEED *= 2;
    return true;
  }

  upgradeTankFireRate() {
    if (!this.canAffordUpgrade(this.upgradeCosts.TANK_FIRE_RATE)) {
      return false;
    }
    this.coins -= this.upgradeCosts.TANK_FIRE_RATE;
    this.tankFireRate *= 1.2;
    this.upgradeCosts.TANK_FIRE_RATE *= 2;
    return true;
  }

  upgradeMaxTanks() {
    if (!this.canAffordUpgrade(this.upgradeCosts.MAX_TANKS)) {
      return false;
    }
    this.coins -= this.upgradeCosts.MAX_TANKS;
    this.maxTanks += 1;
    this.upgradeCosts.MAX_TANKS *= 2;
    return true;
  }

  upgradeMultiShot() {
    if (!this.canAffordUpgrade(this.upgradeCosts.MULTI_SHOT)) {
      return false;
    }
    this.coins -= this.upgradeCosts.MULTI_SHOT;
    this.multiShot += 1;
    this.upgradeCosts.MULTI_SHOT *= 2;
    return true;
  }

  upgradeBaseCoinValue() {
    if (!this.canAffordUpgrade(this.upgradeCosts.BASE_COIN_VALUE)) {
      return false;
    }
    this.coins -= this.upgradeCosts.BASE_COIN_VALUE;
    this.baseCoinValue *= 1.5;
    this.upgradeCosts.BASE_COIN_VALUE *= 2;
    return true;
  }

  destroy() {
    this.app.destroy(true);
  }
}
