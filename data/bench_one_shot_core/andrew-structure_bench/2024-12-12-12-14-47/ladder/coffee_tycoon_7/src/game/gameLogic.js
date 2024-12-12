import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, POSITIONS } from './gameData';
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
    this.effects = new EffectsLibrary(this.app);

    this.ready = false;
    this.money = 0;
    this.baristaCount = INITIAL_VALUES.BARISTA_COUNT;
    this.machineCount = INITIAL_VALUES.MACHINE_COUNT;
    this.baristaSpeed = INITIAL_VALUES.BARISTA_SPEED;
    this.maxCustomers = INITIAL_VALUES.MAX_CUSTOMERS;
    this.coffeeQuality = INITIAL_VALUES.COFFEE_QUALITY;
    
    this.customerSpawnTimer = 0;
    this.lastTimestamp = performance.now();

    this.upgradeCosts = {
      barista: UPGRADE_COSTS.BARISTA,
      machine: UPGRADE_COSTS.MACHINE,
      speed: UPGRADE_COSTS.SPEED,
      space: UPGRADE_COSTS.SPACE,
      quality: UPGRADE_COSTS.QUALITY
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
    this.customers = new PIXI.Container();
    this.baristas = new PIXI.Container();
    this.machines = new PIXI.Container();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.customers);
    this.app.stage.addChild(this.baristas);
    this.app.stage.addChild(this.machines);

    // Create initial baristas and machines
    for (let i = 0; i < this.baristaCount; i++) {
      this.createBarista();
    }
    for (let i = 0; i < this.machineCount; i++) {
      this.createMachine(i);
    }
  }

  createCustomer() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.customer);
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    // Add shadow
    this.effects.createShadow(container, sprite);

    container.x = POSITIONS.ENTRANCE.x;
    container.y = POSITIONS.ENTRANCE.y;
    container.state = 'moving_to_counter';
    container.waitTime = 0;
    container.sprite = sprite;

    this.customers.addChild(container);
    this.effects.spawnAnimation(container);
  }

  createBarista() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.barista);
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    // Add shadow
    const shadow = this.effects.createShadow(container, sprite);
    this.effects.idleAnimation(shadow);

    container.x = POSITIONS.COUNTER.x;
    container.y = POSITIONS.COUNTER.y;
    container.state = 'idle';
    container.targetMachine = null;
    container.targetCustomer = null;
    container.sprite = sprite;

    this.baristas.addChild(container);
    this.effects.spawnAnimation(container);
  }

  createMachine(index) {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.machine);
    sprite.anchor.set(0.5);
    container.addChild(sprite);

    container.x = POSITIONS.MACHINE_START.x + (index * POSITIONS.MACHINE_SPACING);
    container.y = POSITIONS.MACHINE_START.y;
    container.inUse = false;
    container.sprite = sprite;

    this.machines.addChild(container);
    this.effects.spawnAnimation(container);
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.customerSpawnTimer += elapsedSecs;
    if (this.customerSpawnTimer >= INITIAL_VALUES.CUSTOMER_SPAWN_TIME && 
        this.customers.children.length < this.maxCustomers) {
      this.createCustomer();
      this.customerSpawnTimer = 0;
    }

    this.updateCustomers(elapsedSecs);
    this.updateBaristas(elapsedSecs);
  }

  updateCustomers(elapsedSecs) {
    this.customers.children.forEach(customer => {
      if (customer.state === 'moving_to_counter') {
        const dx = POSITIONS.COUNTER.x - customer.x;
        const dy = POSITIONS.COUNTER.y - customer.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 5) {
          customer.x += (dx / distance) * INITIAL_VALUES.BARISTA_SPEED * elapsedSecs;
          customer.y += (dy / distance) * INITIAL_VALUES.BARISTA_SPEED * elapsedSecs;
        } else {
          customer.state = 'waiting';
          this.effects.createParticleSystem(customer, {
            maxParticles: 10,
            spawnInterval: 5,
            radius: 20
          });
        }
      } else if (customer.state === 'leaving') {
        const dx = POSITIONS.EXIT.x - customer.x;
        const dy = POSITIONS.EXIT.y - customer.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 5) {
          customer.x += (dx / distance) * INITIAL_VALUES.BARISTA_SPEED * elapsedSecs;
          customer.y += (dy / distance) * INITIAL_VALUES.BARISTA_SPEED * elapsedSecs;
        } else {
          if (customer.satisfied) {
            this.effects.createSpiralParticles(this.app.stage, {
              x: customer.x,
              y: customer.y
            });
          }
          this.customers.removeChild(customer);
        }
      } else if (customer.state === 'waiting') {
        customer.waitTime += elapsedSecs;
        if (customer.waitTime >= INITIAL_VALUES.CUSTOMER_PATIENCE) {
          customer.state = 'leaving';
          customer.satisfied = false;
          this.effects.createExplosionParticles(this.app.stage, {
            x: customer.x,
            y: customer.y,
            color: 0xFF0000
          });
        }
      }
    });
  }

  updateBaristas(elapsedSecs) {
    this.baristas.children.forEach(barista => {
      if (barista.state === 'idle') {
        const waitingCustomer = this.customers.children.find(c => c.state === 'waiting' && !c.beingServed);
        const freeMachine = this.machines.children.find(m => !m.inUse);
        
        if (waitingCustomer && freeMachine) {
          barista.state = 'moving_to_machine';
          barista.targetMachine = freeMachine;
          barista.targetCustomer = waitingCustomer;
          waitingCustomer.beingServed = true;
          freeMachine.inUse = true;
        }
      } else if (barista.state === 'moving_to_machine') {
        const dx = barista.targetMachine.x - barista.x;
        const dy = barista.targetMachine.y - barista.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 5) {
          barista.x += (dx / distance) * this.baristaSpeed * elapsedSecs;
          barista.y += (dy / distance) * this.baristaSpeed * elapsedSecs;
        } else {
          barista.state = 'preparing';
          barista.prepTime = 0;
          this.effects.createParticleSystem(barista.targetMachine, {
            maxParticles: 20,
            spawnInterval: 2,
            radius: 30
          });
        }
      } else if (barista.state === 'preparing') {
        barista.prepTime += elapsedSecs;
        if (barista.prepTime >= INITIAL_VALUES.COFFEE_PREP_TIME) {
          barista.state = 'serving';
          this.effects.createImpactEffect(this.app.stage, {
            x: barista.x,
            y: barista.y,
            color: 0x8B4513
          });
        }
      } else if (barista.state === 'serving') {
        const dx = POSITIONS.COUNTER.x - barista.x;
        const dy = POSITIONS.COUNTER.y - barista.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 5) {
          barista.x += (dx / distance) * this.baristaSpeed * elapsedSecs;
          barista.y += (dy / distance) * this.baristaSpeed * elapsedSecs;
        } else {
          const earnedMoney = INITIAL_VALUES.BASE_COFFEE_PRICE * this.coffeeQuality;
          this.money += earnedMoney;
          this.effects.showFloatingText(barista, `+$${Math.floor(earnedMoney)}`);
          
          barista.targetMachine.inUse = false;
          barista.targetCustomer.state = 'leaving';
          barista.targetCustomer.satisfied = true;
          barista.state = 'idle';
          barista.targetMachine = null;
          barista.targetCustomer = null;
        }
      }
    });
  }

  upgradeBaristas() {
    if (this.money >= this.upgradeCosts.barista) {
      this.money -= this.upgradeCosts.barista;
      this.createBarista();
      this.baristaCount++;
      this.upgradeCosts.barista *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 5 });
    }
  }

  upgradeMachines() {
    if (this.money >= this.upgradeCosts.machine) {
      this.money -= this.upgradeCosts.machine;
      this.createMachine(this.machineCount);
      this.machineCount++;
      this.upgradeCosts.machine *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 5 });
    }
  }

  upgradeSpeed() {
    if (this.money >= this.upgradeCosts.speed) {
      this.money -= this.upgradeCosts.speed;
      this.baristaSpeed *= 1.2;
      this.upgradeCosts.speed *= 2;
      this.baristas.children.forEach(barista => {
        this.effects.flashColor(barista.sprite, { color: 0xFFFF00 });
      });
    }
  }

  upgradeSpace() {
    if (this.money >= this.upgradeCosts.space) {
      this.money -= this.upgradeCosts.space;
      this.maxCustomers += 2;
      this.upgradeCosts.space *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 8 });
    }
  }

  upgradeQuality() {
    if (this.money >= this.upgradeCosts.quality) {
      this.money -= this.upgradeCosts.quality;
      this.coffeeQuality *= 1.2;
      this.upgradeCosts.quality *= 2;
      this.machines.children.forEach(machine => {
        this.effects.createSpiralParticles(machine, {
          color: 0xFFD700
        });
      });
    }
  }

  getSprite(spriteConfig) {
    const texture = PIXI.Texture.from(spriteConfig.path);
    const sprite = new PIXI.Sprite(texture);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    return sprite;
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
