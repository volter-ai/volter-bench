import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, ENEMY_CONFIG } from './gameData';
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
    this.fireRate = INITIAL_VALUES.FIRE_RATE;
    this.detectionRange = INITIAL_VALUES.DETECTION_RANGE;
    this.tankCount = INITIAL_VALUES.TANK_COUNT;
    
    this.costs = {...UPGRADE_COSTS};
    this.enemySpawnTimer = 0;
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
    this.friendlyTanks = new PIXI.Container();
    this.enemyTanks = new PIXI.Container();
    this.bullets = new PIXI.Container();
    this.healthBars = new PIXI.Container();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.friendlyTanks);
    this.app.stage.addChild(this.enemyTanks);
    this.app.stage.addChild(this.bullets);
    this.app.stage.addChild(this.healthBars);

    for (let i = 0; i < this.tankCount; i++) {
      this.createFriendlyTank();
    }
  }

  createFriendlyTank() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.friendlyTank);
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    // Create shadow
    this.effects.createShadow(container, sprite, {
      widthRatio: 0.8,
      heightRatio: 0.2,
      alpha: 0.2
    });

    container.x = Math.random() * (this.app.screen.width / 2);
    container.y = Math.random() * this.app.screen.height;
    container.health = this.tankHealth;
    container.shootTimer = 0;
    container.targetX = Math.random() * (this.app.screen.width / 2);
    container.targetY = Math.random() * this.app.screen.height;
    
    // Store sprite reference and add spawn animation
    container.sprite = sprite;
    this.effects.spawnAnimation(container, {
      initialScale: { x: 0.5, y: 1.5 },
      finalScale: { x: 1, y: 1 },
      duration: 0.5
    });

    this.friendlyTanks.addChild(container);
  }

  createEnemyTank() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.enemyTank);
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    // Create shadow
    this.effects.createShadow(container, sprite, {
      widthRatio: 0.8,
      heightRatio: 0.2,
      alpha: 0.2
    });

    container.x = this.app.screen.width;
    container.y = Math.random() * this.app.screen.height;
    container.health = ENEMY_CONFIG.HEALTH;
    container.shootTimer = 0;
    
    const healthBar = new PIXI.Graphics();
    healthBar.tank = container;
    this.healthBars.addChild(healthBar);
    container.healthBar = healthBar;
    
    // Store sprite reference and add spawn animation
    container.sprite = sprite;
    this.effects.spawnAnimation(container, {
      initialScale: { x: 0.5, y: 1.5 },
      finalScale: { x: 1, y: 1 },
      duration: 0.5
    });

    this.enemyTanks.addChild(container);
  }

  createBullet(x, y, targetX, targetY, friendly) {
    const bullet = new PIXI.Graphics();
    bullet.beginFill(friendly ? 0x00ff88 : 0xff3333);
    bullet.drawCircle(0, 0, 3);
    bullet.endFill();
    bullet.x = x;
    bullet.y = y;
    
    const angle = Math.atan2(targetY - y, targetX - x);
    bullet.dx = Math.cos(angle) * INITIAL_VALUES.BULLET_SPEED;
    bullet.dy = Math.sin(angle) * INITIAL_VALUES.BULLET_SPEED;
    bullet.friendly = friendly;
    bullet.damage = friendly ? this.tankDamage : ENEMY_CONFIG.DAMAGE;
    
    // Create muzzle flash
    this.effects.createImpactEffect(this.bullets, {
      x: x,
      y: y,
      radius: 10,
      color: friendly ? 0x00ff88 : 0xff3333,
      duration: 0.1,
      alpha: 0.5
    });

    this.bullets.addChild(bullet);
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.updateTanks(elapsedSecs);
    this.updateBullets(elapsedSecs);
    this.updateHealthBars();
    this.spawnEnemies(elapsedSecs);
  }

  updateTanks(elapsedSecs) {
    this.friendlyTanks.children.forEach(tank => {
      tank.shootTimer -= elapsedSecs;
      
      let nearestEnemy = null;
      let minDist = this.detectionRange;
      
      this.enemyTanks.children.forEach(enemy => {
        const dist = Math.hypot(enemy.x - tank.x, enemy.y - tank.y);
        if (dist < minDist) {
          minDist = dist;
          nearestEnemy = enemy;
        }
      });

      if (nearestEnemy) {
        tank.targetX = nearestEnemy.x;
        tank.targetY = nearestEnemy.y;
        
        if (tank.shootTimer <= 0) {
          this.createBullet(tank.x, tank.y, nearestEnemy.x, nearestEnemy.y, true);
          tank.shootTimer = 1 / this.fireRate;
        }
      } else if (Math.hypot(tank.targetX - tank.x, tank.targetY - tank.y) < 10) {
        tank.targetX = Math.random() * (this.app.screen.width / 2);
        tank.targetY = Math.random() * this.app.screen.height;
      }

      const angle = Math.atan2(tank.targetY - tank.y, tank.targetX - tank.x);
      tank.rotation = angle + Math.PI/2;
      
      const speed = nearestEnemy ? this.tankSpeed : this.tankSpeed * 0.5;
      tank.x += Math.cos(angle) * speed * elapsedSecs;
      tank.y += Math.sin(angle) * speed * elapsedSecs;
    });

    this.enemyTanks.children.forEach(tank => {
      tank.shootTimer -= elapsedSecs;
      
      const nearestFriendly = this.friendlyTanks.children[0];
      if (nearestFriendly) {
        const angle = Math.atan2(nearestFriendly.y - tank.y, nearestFriendly.x - tank.x);
        tank.rotation = angle + Math.PI/2;
        
        tank.x += Math.cos(angle) * ENEMY_CONFIG.SPEED * elapsedSecs;
        tank.y += Math.sin(angle) * ENEMY_CONFIG.SPEED * elapsedSecs;
        
        if (tank.shootTimer <= 0) {
          this.createBullet(tank.x, tank.y, nearestFriendly.x, nearestFriendly.y, false);
          tank.shootTimer = 1 / ENEMY_CONFIG.FIRE_RATE;
        }
      }
    });
  }

  updateBullets(elapsedSecs) {
    this.bullets.children.forEach(bullet => {
      bullet.x += bullet.dx * elapsedSecs;
      bullet.y += bullet.dy * elapsedSecs;
      
      if (bullet.x < 0 || bullet.x > this.app.screen.width || 
          bullet.y < 0 || bullet.y > this.app.screen.height) {
        this.bullets.removeChild(bullet);
        return;
      }

      const targets = bullet.friendly ? this.enemyTanks : this.friendlyTanks;
      targets.children.forEach(tank => {
        if (Math.hypot(tank.x - bullet.x, tank.y - bullet.y) < 32) {
          tank.health -= bullet.damage;
          this.bullets.removeChild(bullet);
          
          // Impact effect
          this.effects.createImpactEffect(this.app.stage, {
            x: bullet.x,
            y: bullet.y,
            radius: 20,
            color: bullet.friendly ? 0x00ff88 : 0xff3333,
            duration: 0.2
          });

          // Flash tank on hit
          this.effects.flashColor(tank.sprite, {
            color: bullet.friendly ? 0x00ff88 : 0xff3333,
            flashDuration: 0.1
          });

          // Show damage number
          this.effects.showFloatingText(tank, `-${bullet.damage}`, {
            color: bullet.friendly ? 0x00ff88 : 0xff3333,
            fontSize: 16
          });
          
          if (tank.health <= 0) {
            if (!bullet.friendly) {
              tank.health = this.tankHealth;
              tank.x = Math.random() * (this.app.screen.width / 2);
              tank.y = Math.random() * this.app.screen.height;
            } else {
              // Death explosion
              this.effects.createExplosionParticles(this.app.stage, {
                x: tank.x,
                y: tank.y,
                count: 30,
                color: 0xff3333
              });

              this.credits += INITIAL_VALUES.CREDITS_PER_KILL;
              // Show credits earned
              this.effects.showFloatingText(tank, `+${INITIAL_VALUES.CREDITS_PER_KILL}`, {
                color: 0xffff00,
                fontSize: 20
              });

              this.enemyTanks.removeChild(tank);
              this.healthBars.removeChild(tank.healthBar);
            }
          }
        }
      });
    });
  }

  updateHealthBars() {
    this.healthBars.children.forEach(bar => {
      const tank = bar.tank;
      bar.clear();
      bar.beginFill(0xff0000);
      bar.drawRect(tank.x - 32, tank.y - 40, 64, 5);
      bar.beginFill(0x00ff00);
      bar.drawRect(tank.x - 32, tank.y - 40, 64 * (tank.health / ENEMY_CONFIG.HEALTH), 5);
    });
  }

  spawnEnemies(elapsedSecs) {
    this.enemySpawnTimer -= elapsedSecs;
    if (this.enemySpawnTimer <= 0) {
      this.createEnemyTank();
      this.enemySpawnTimer = INITIAL_VALUES.ENEMY_SPAWN_RATE;
    }
  }

  upgradeTankCount() {
    if (this.credits >= this.costs.TANK_COUNT) {
      this.credits -= this.costs.TANK_COUNT;
      this.tankCount++;
      this.createFriendlyTank();
      this.costs.TANK_COUNT *= 2;
    }
  }

  upgradeTankSpeed() {
    if (this.credits >= this.costs.TANK_SPEED) {
      this.credits -= this.costs.TANK_SPEED;
      this.tankSpeed *= 1.2;
      this.costs.TANK_SPEED *= 2;
      
      // Highlight effect on all tanks
      this.friendlyTanks.children.forEach(tank => {
        this.effects.highlightCharacter(tank.sprite, {
          color: 0x00ff88,
          duration: 0.3
        });
      });
    }
  }

  upgradeTankDamage() {
    if (this.credits >= this.costs.TANK_DAMAGE) {
      this.credits -= this.costs.TANK_DAMAGE;
      this.tankDamage *= 1.2;
      this.costs.TANK_DAMAGE *= 2;
      
      // Highlight effect on all tanks
      this.friendlyTanks.children.forEach(tank => {
        this.effects.highlightCharacter(tank.sprite, {
          color: 0xff3333,
          duration: 0.3
        });
      });
    }
  }

  upgradeTankHealth() {
    if (this.credits >= this.costs.TANK_HEALTH) {
      this.credits -= this.costs.TANK_HEALTH;
      this.tankHealth *= 1.2;
      this.friendlyTanks.children.forEach(tank => {
        tank.health = this.tankHealth;
        this.effects.highlightCharacter(tank.sprite, {
          color: 0x00ff00,
          duration: 0.3
        });
      });
      this.costs.TANK_HEALTH *= 2;
    }
  }

  upgradeFireRate() {
    if (this.credits >= this.costs.FIRE_RATE) {
      this.credits -= this.costs.FIRE_RATE;
      this.fireRate *= 1.2;
      this.costs.FIRE_RATE *= 2;
      
      // Highlight effect on all tanks
      this.friendlyTanks.children.forEach(tank => {
        this.effects.highlightCharacter(tank.sprite, {
          color: 0xffff00,
          duration: 0.3
        });
      });
    }
  }

  upgradeDetectionRange() {
    if (this.credits >= this.costs.DETECTION_RANGE) {
      this.credits -= this.costs.DETECTION_RANGE;
      this.detectionRange *= 1.2;
      this.costs.DETECTION_RANGE *= 2;
      
      // Highlight effect on all tanks
      this.friendlyTanks.children.forEach(tank => {
        this.effects.highlightCharacter(tank.sprite, {
          color: 0x00ffff,
          duration: 0.3
        });
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
