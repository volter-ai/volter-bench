import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, STATION_POSITIONS } from './gameData';
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
    this.money = 100;
    this.baristaSpeed = INITIAL_VALUES.BARISTA_SPEED;
    this.baristaCount = INITIAL_VALUES.BARISTA_COUNT;
    this.coffeeTime = INITIAL_VALUES.COFFEE_PREP_TIME;
    this.serviceTime = INITIAL_VALUES.SERVICE_TIME;
    this.counterCount = INITIAL_VALUES.COUNTER_COUNT;
    this.paymentAmount = INITIAL_VALUES.PAYMENT_AMOUNT;

    this.upgradeCosts = {...UPGRADE_COSTS};
    this.lastTimestamp = performance.now();
    this.counterStates = new Array(3).fill(false);

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(spriteKey) {
    const texture = PIXI.Loader.shared.resources[spriteKey].texture;
    const sprite = new PIXI.Sprite(texture);
    sprite.width = SPRITES[spriteKey].width;
    sprite.height = SPRITES[spriteKey].height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite('background');
    this.baristas = new PIXI.Container();
    this.customers = new PIXI.Container();
    this.stations = new PIXI.Container();

    this.createBarista();
    this.createStations();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.stations);
    this.app.stage.addChild(this.customers);
    this.app.stage.addChild(this.baristas);
  }

  createBarista() {
    const container = new PIXI.Container();
    const sprite = this.getSprite('barista');
    sprite.anchor.set(0.5);
    
    // Add shadow
    this.effects.createShadow(container, sprite);
    container.addChild(sprite);

    container.x = STATION_POSITIONS.IDLE_POSITION.x;
    container.y = STATION_POSITIONS.IDLE_POSITION.y;
    container.state = 'idle';
    container.targetX = container.x;
    container.targetY = container.y;
    container.sprite = sprite;

    this.effects.spawnAnimation(container);
    this.effects.idleAnimation(sprite);
    
    this.baristas.addChild(container);
  }

  createStations() {
    for (let i = 0; i < 3; i++) {
      const container = new PIXI.Container();
      const counter = this.getSprite('counter');
      counter.anchor.set(0.5);
      
      this.effects.createShadow(container, counter);
      container.addChild(counter);
      
      container.x = STATION_POSITIONS.ORDER_COUNTERS[i].x;
      container.y = STATION_POSITIONS.ORDER_COUNTERS[i].y;
      container.occupied = false;
      this.stations.addChild(container);
    }

    for (let i = 0; i < 3; i++) {
      const container = new PIXI.Container();
      const machine = this.getSprite('coffee_machine');
      machine.anchor.set(0.5);
      
      this.effects.createShadow(container, machine);
      container.addChild(machine);
      
      container.x = STATION_POSITIONS.COFFEE_MACHINES[i].x;
      container.y = STATION_POSITIONS.COFFEE_MACHINES[i].y;
      container.occupied = false;
      container.sprite = machine;
      this.stations.addChild(container);
    }
  }

  spawnCustomer() {
    if (this.customers.children.length >= this.counterCount) {
      return;
    }

    for (let i = 0; i < this.counterCount; i++) {
      if (!this.counterStates[i]) {
        const counterPos = STATION_POSITIONS.ORDER_COUNTERS[i];
        const container = new PIXI.Container();
        const customer = this.getSprite('customer');
        customer.anchor.set(0.5);
        
        this.effects.createShadow(container, customer);
        container.addChild(customer);
        
        container.x = counterPos.x;
        container.y = counterPos.y;
        container.state = 'waiting';
        container.counterId = i;
        container.sprite = customer;
        
        this.effects.spawnAnimation(container);
        this.effects.createSpiralParticles(container, {
          x: 0,
          y: -customer.height/2
        });
        
        this.customers.addChild(container);
        this.counterStates[i] = true;
        break;
      }
    }
  }

  moveEntity(entity, targetX, targetY, speed, elapsedSecs) {
    const dx = targetX - entity.x;
    const dy = targetY - entity.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance > 1) {
      const moveDistance = speed * elapsedSecs;
      const ratio = moveDistance / distance;
      entity.x += dx * ratio;
      entity.y += dy * ratio;
      
      // Create movement particles
      if (entity.state.includes('moving')) {
        this.effects.createParticleSystem(entity, {
          maxParticles: 10,
          spawnInterval: 5,
          radius: 10
        });
      }
      
      return false;
    }
    
    entity.x = targetX;
    entity.y = targetY;
    return true;
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.spawnCustomer();

    this.baristas.children.forEach(barista => {
      if (barista.state === 'idle') {
        const waitingCustomer = this.customers.children.find(c => c.state === 'waiting');
        if (waitingCustomer) {
          barista.state = 'moving_to_customer';
          barista.targetX = waitingCustomer.x;
          barista.targetY = waitingCustomer.y;
          barista.servingCustomerId = waitingCustomer.counterId;
          waitingCustomer.state = 'being_served';
        }
      }
      
      if (barista.state === 'moving_to_customer' || barista.state === 'moving_to_machine' || 
          barista.state === 'moving_to_service' || barista.state === 'returning') {
        const arrived = this.moveEntity(barista, barista.targetX, barista.targetY, this.baristaSpeed, elapsedSecs);
        if (arrived) {
          if (barista.state === 'moving_to_customer') {
            barista.state = 'moving_to_machine';
            const machine = STATION_POSITIONS.COFFEE_MACHINES[0];
            barista.targetX = machine.x;
            barista.targetY = machine.y;
          } else if (barista.state === 'moving_to_machine') {
            barista.state = 'preparing';
            barista.timer = this.coffeeTime;
            // Start coffee preparation effects
            this.effects.createSpiralParticles(barista, {
              y: -barista.sprite.height,
              color: 0x8B4513
            });
          } else if (barista.state === 'moving_to_service') {
            barista.state = 'serving';
            barista.timer = this.serviceTime;
          } else if (barista.state === 'returning') {
            barista.state = 'idle';
          }
        }
      }

      if (barista.state === 'preparing' || barista.state === 'serving') {
        barista.timer -= elapsedSecs;
        if (barista.timer <= 0) {
          if (barista.state === 'preparing') {
            barista.state = 'moving_to_service';
            const service = STATION_POSITIONS.SERVICE_COUNTERS[0];
            barista.targetX = service.x;
            barista.targetY = service.y;
          } else if (barista.state === 'serving') {
            this.money += this.paymentAmount;
            
            // Payment effects
            this.effects.showFloatingText(barista, `+$${this.paymentAmount}`);
            this.effects.createExplosionParticles(barista, {
              color: 0xFFD700,
              count: 20
            });
            
            barista.state = 'returning';
            barista.targetX = STATION_POSITIONS.IDLE_POSITION.x;
            barista.targetY = STATION_POSITIONS.IDLE_POSITION.y;
            
            const servedCustomer = this.customers.children.find(c => c.state === 'being_served');
            if (servedCustomer) {
              this.counterStates[servedCustomer.counterId] = false;
              this.customers.removeChild(servedCustomer);
            }
          }
        }
      }
    });
  }

  upgradeBaristas() {
    if (this.money >= this.upgradeCosts.BARISTA) {
      this.money -= this.upgradeCosts.BARISTA;
      this.createBarista();
      this.baristaCount++;
      this.upgradeCosts.BARISTA *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 5 });
    }
  }

  upgradeBaristaSpeed() {
    if (this.money >= this.upgradeCosts.BARISTA_SPEED) {
      this.money -= this.upgradeCosts.BARISTA_SPEED;
      this.baristaSpeed *= 1.2;
      this.upgradeCosts.BARISTA_SPEED *= 2;
      this.baristas.children.forEach(barista => {
        this.effects.flashColor(barista.sprite, { color: 0x00FF00 });
      });
    }
  }

  upgradeCoffeeMachine() {
    if (this.money >= this.upgradeCosts.COFFEE_MACHINE) {
      this.money -= this.upgradeCosts.COFFEE_MACHINE;
      this.coffeeTime *= 0.8;
      this.upgradeCosts.COFFEE_MACHINE *= 2;
      this.stations.children.forEach(station => {
        if (station.sprite && station.sprite.texture === PIXI.Loader.shared.resources['coffee_machine'].texture) {
          this.effects.flashColor(station.sprite, { color: 0x00FF00 });
        }
      });
    }
  }

  upgradeCounter() {
    if (this.money >= this.upgradeCosts.COUNTER) {
      this.money -= this.upgradeCosts.COUNTER;
      this.counterCount++;
      this.upgradeCosts.COUNTER *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 5 });
    }
  }

  upgradePrices() {
    if (this.money >= this.upgradeCosts.PREMIUM_PRICES) {
      this.money -= this.upgradeCosts.PREMIUM_PRICES;
      this.paymentAmount *= 1.5;
      this.upgradeCosts.PREMIUM_PRICES *= 2;
      this.effects.createExplosionParticles(this.app.stage, {
        x: SCREEN_SIZE.width/2,
        y: SCREEN_SIZE.height/2,
        color: 0xFFD700
      });
    }
  }

  upgradeTraining() {
    if (this.money >= this.upgradeCosts.TRAINING) {
      this.money -= this.upgradeCosts.TRAINING;
      this.serviceTime *= 0.8;
      this.upgradeCosts.TRAINING *= 2;
      this.baristas.children.forEach(barista => {
        this.effects.createSpiralParticles(barista, {
          color: 0x00FF00
        });
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
