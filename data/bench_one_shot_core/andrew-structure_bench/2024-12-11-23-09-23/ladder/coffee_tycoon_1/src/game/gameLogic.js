import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, POSITIONS, MOVEMENT_POINTS } from './gameData';
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
    this.money = 0;
    this.baristaSpeed = INITIAL_VALUES.BARISTA_SPEED;
    this.coffeeMakeTime = INITIAL_VALUES.COFFEE_MAKE_TIME;
    this.coffeePrice = INITIAL_VALUES.COFFEE_PRICE;
    this.customerCapacity = INITIAL_VALUES.CUSTOMER_CAPACITY;
    this.baristaCount = INITIAL_VALUES.BARISTA_COUNT;

    this.upgradeCosts = {
      barista: UPGRADE_COSTS.BARISTA,
      speed: UPGRADE_COSTS.SPEED,
      efficiency: UPGRADE_COSTS.COFFEE_EFFICIENCY,
      capacity: UPGRADE_COSTS.CAPACITY,
      price: UPGRADE_COSTS.PRICE
    };

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  createGameObjects() {
    this.background = this.getSprite(SPRITES.background);
    
    // Create coffee machine container
    this.coffeeMachineContainer = new PIXI.Container();
    this.coffeeMachine = this.getSprite(SPRITES.coffee_machine);
    this.coffeeMachineContainer.addChild(this.coffeeMachine);
    this.effects.createShadow(this.coffeeMachineContainer, this.coffeeMachine);
    this.coffeeMachineContainer.position.set(POSITIONS.COFFEE_MACHINE.x, POSITIONS.COFFEE_MACHINE.y);

    this.baristas = new PIXI.Container();
    this.customers = new PIXI.Container();
    this.customerQueue = [];

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.coffeeMachineContainer);
    this.app.stage.addChild(this.baristas);
    this.app.stage.addChild(this.customers);

    this.createBarista();
    this.spawnCustomer();
  }

  getSprite(spriteConfig) {
    const texture = PIXI.Texture.from(spriteConfig.path);
    const sprite = new PIXI.Sprite(texture);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    return sprite;
  }

  createBarista() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.barista);
    sprite.anchor.set(0.5);
    container.addChild(sprite);
    
    // Add shadow
    this.effects.createShadow(container, sprite);
    
    container.position.set(MOVEMENT_POINTS.START.x, MOVEMENT_POINTS.START.y);
    container.state = 'idle';
    container.targetCustomer = null;
    container.coffeeTimer = 0;
    container.sprite = sprite;
    
    this.baristas.addChild(container);
    
    // Spawn effect
    this.effects.spawnAnimation(container);
    this.effects.createExplosionParticles(this.app.stage, {
      x: container.x,
      y: container.y,
      color: 0xE6B17E
    });
  }

  spawnCustomer() {
    if (this.customerQueue.length >= this.customerCapacity) return;

    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.customer);
    sprite.anchor.set(0.5);
    container.addChild(sprite);
    
    // Add shadow
    this.effects.createShadow(container, sprite);
    
    container.position.set(
      POSITIONS.CUSTOMER_COUNTER.x,
      POSITIONS.CUSTOMER_COUNTER.y + this.customerQueue.length * POSITIONS.CUSTOMER_SPACING
    );
    container.state = 'waiting';
    container.sprite = sprite;
    
    this.customers.addChild(container);
    this.customerQueue.push(container);
    
    // Spawn effect
    this.effects.spawnAnimation(container);
  }

  moveTowards(object, target, speed, delta) {
    const dx = target.x - object.x;
    const dy = target.y - object.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance < 1) return true;

    const movement = speed * delta;
    object.x += (dx / distance) * movement;
    object.y += (dy / distance) * movement;
    
    // Create footstep particles while moving
    if (Math.random() < 0.1) {
      this.effects.createImpactEffect(this.app.stage, {
        x: object.x,
        y: object.y + 30,
        radius: 5,
        color: 0x444444,
        alpha: 0.3
      });
    }
    
    return false;
  }

  gameLoop(delta) {
    const elapsedSecs = delta / 60;

    this.baristas.children.forEach(barista => {
      switch(barista.state) {
        case 'idle':
          if (this.customerQueue.length > 0) {
            barista.targetCustomer = this.customerQueue[0];
            barista.state = 'moving_to_machine';
          }
          break;

        case 'moving_to_machine':
          if (this.moveTowards(barista, MOVEMENT_POINTS.COFFEE_MACHINE, this.baristaSpeed, elapsedSecs)) {
            barista.state = 'making_coffee';
            barista.coffeeTimer = 0;
            
            // Start coffee making particles
            this.effects.createSpiralParticles(this.app.stage, {
              x: this.coffeeMachineContainer.x,
              y: this.coffeeMachineContainer.y - 50,
              color: 0xE6B17E
            });
          }
          break;

        case 'making_coffee':
          barista.coffeeTimer += elapsedSecs;
          if (barista.coffeeTimer >= this.coffeeMakeTime) {
            barista.state = 'serving';
            
            // Coffee ready effect
            this.effects.createImpactEffect(this.app.stage, {
              x: this.coffeeMachineContainer.x,
              y: this.coffeeMachineContainer.y,
              color: 0xFFFFFF
            });
          }
          break;

        case 'serving':
          if (this.moveTowards(barista, MOVEMENT_POINTS.SERVING, this.baristaSpeed, elapsedSecs)) {
            this.money += this.coffeePrice;
            
            // Show floating money text
            this.effects.showFloatingText(barista, `+$${this.coffeePrice}`, {
              color: 0x00FF00
            });
            
            const servedCustomer = this.customerQueue.shift();
            
            // Customer leave effect
            this.effects.createExplosionParticles(this.app.stage, {
              x: servedCustomer.x,
              y: servedCustomer.y,
              color: 0xE6B17E
            });
            
            this.customers.removeChild(servedCustomer);
            
            // Animate remaining customers moving forward
            this.customerQueue.forEach((customer, index) => {
              this.effects.plopAnimation(customer, customer.sprite, {
                targetX: POSITIONS.CUSTOMER_COUNTER.x,
                targetY: POSITIONS.CUSTOMER_COUNTER.y + index * POSITIONS.CUSTOMER_SPACING,
                standardHeight: 64
              });
            });
            
            barista.state = 'returning';
            this.spawnCustomer();
          }
          break;

        case 'returning':
          if (this.moveTowards(barista, MOVEMENT_POINTS.START, this.baristaSpeed, elapsedSecs)) {
            barista.state = 'idle';
            barista.targetCustomer = null;
          }
          break;
      }
    });
  }

  upgradeBarista() {
    if (this.money >= this.upgradeCosts.barista) {
      this.money -= this.upgradeCosts.barista;
      this.createBarista();
      this.upgradeCosts.barista *= 2;
      this.baristaCount++;
      this.effects.screenShake(this.app.stage);
    }
  }

  upgradeSpeed() {
    if (this.money >= this.upgradeCosts.speed) {
      this.money -= this.upgradeCosts.speed;
      this.baristaSpeed *= 1.2;
      this.upgradeCosts.speed *= 2;
      
      // Highlight all baristas
      this.baristas.children.forEach(barista => {
        this.effects.highlightCharacter(barista.sprite);
      });
    }
  }

  upgradeEfficiency() {
    if (this.money >= this.upgradeCosts.efficiency) {
      this.money -= this.upgradeCosts.efficiency;
      this.coffeeMakeTime *= 0.8;
      this.upgradeCosts.efficiency *= 2;
      
      // Coffee machine upgrade effect
      this.effects.flashColor(this.coffeeMachine, {
        color: 0xFFFF00
      });
      this.effects.createExplosionParticles(this.app.stage, {
        x: this.coffeeMachineContainer.x,
        y: this.coffeeMachineContainer.y,
        color: 0xFFFF00
      });
    }
  }

  upgradeCapacity() {
    if (this.money >= this.upgradeCosts.capacity) {
      this.money -= this.upgradeCosts.capacity;
      this.customerCapacity++;
      this.upgradeCosts.capacity *= 2;
      this.spawnCustomer();
      this.effects.screenShake(this.app.stage);
    }
  }

  upgradePrice() {
    if (this.money >= this.upgradeCosts.price) {
      this.money -= this.upgradeCosts.price;
      this.coffeePrice = Math.floor(this.coffeePrice * 1.2);
      this.upgradeCosts.price *= 2;
      
      // Price increase effect
      this.effects.showFloatingText(this.coffeeMachineContainer, `$${this.coffeePrice}!`, {
        color: 0xFFD700
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
