import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, STATION_POSITIONS } from './gameData';
import { SPRITES } from './assetManifest';
import { EffectsLibrary } from '../lib/effectsLib';

const SCREEN_SIZE = {
  width: 800,
  height: 600
}

function loadAssets(sprites, onComplete) {
  const loader = new PIXI.Loader();
  
  Object.values(sprites).forEach(sprite => {
    loader.add(sprite.path, sprite.path);
  });

  loader.load(() => {
    onComplete();
  });
}

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
    this.lastTimestamp = performance.now();

    // Game state
    this.baristaCount = INITIAL_VALUES.BARISTA_COUNT;
    this.baristaSpeed = INITIAL_VALUES.BARISTA_SPEED;
    this.coffeeMachineTime = INITIAL_VALUES.COFFEE_MACHINE_TIME;
    this.counterCount = INITIAL_VALUES.COUNTER_COUNT;
    this.coffeePrice = INITIAL_VALUES.COFFEE_PRICE;
    this.customerSpawnTime = INITIAL_VALUES.CUSTOMER_SPAWN_TIME;

    // Upgrade costs
    this.baristaCountCost = UPGRADE_COSTS.BARISTA_COUNT;
    this.baristaSpeedCost = UPGRADE_COSTS.BARISTA_SPEED;
    this.coffeeMachineCost = UPGRADE_COSTS.COFFEE_MACHINE;
    this.counterCountCost = UPGRADE_COSTS.COUNTER_COUNT;
    this.coffeePriceCost = UPGRADE_COSTS.COFFEE_PRICE;
    this.customerAttractionCost = UPGRADE_COSTS.CUSTOMER_ATTRACTION;

    // Timers
    this.customerSpawnTimer = 0;

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  createGameObjects() {
    this.background = this.getSprite(SPRITES.background);
    this.app.stage.addChild(this.background);

    // Create containers
    this.counters = new PIXI.Container();
    this.coffeeMachines = new PIXI.Container();
    this.baristas = new PIXI.Container();
    this.customers = new PIXI.Container();

    this.app.stage.addChild(this.counters);
    this.app.stage.addChild(this.coffeeMachines);
    this.app.stage.addChild(this.baristas);
    this.app.stage.addChild(this.customers);

    // Initialize stations
    this.createInitialStations();
    this.createInitialBaristas();
  }

  createInitialStations() {
    for (let i = 0; i < this.counterCount; i++) {
      const counterContainer = new PIXI.Container();
      const counter = this.getSprite(SPRITES.counter);
      counterContainer.addChild(counter);
      counterContainer.x = STATION_POSITIONS.COUNTER_START_X + (i * STATION_POSITIONS.COUNTER_SPACING);
      counterContainer.y = STATION_POSITIONS.COUNTER_Y;
      counterContainer.customer = null;
      this.counters.addChild(counterContainer);

      const machineContainer = new PIXI.Container();
      const machine = this.getSprite(SPRITES.coffeeMachine);
      machineContainer.addChild(machine);
      machineContainer.x = STATION_POSITIONS.MACHINE_START_X + (i * STATION_POSITIONS.MACHINE_SPACING);
      machineContainer.y = STATION_POSITIONS.MACHINE_Y;
      machineContainer.inUse = false;
      this.coffeeMachines.addChild(machineContainer);

      // Add shadow to counter
      this.effects.createShadow(counterContainer, counter, { offsetY: 10 });
      this.effects.createShadow(machineContainer, machine, { offsetY: 5 });
    }
  }

  createInitialBaristas() {
    for (let i = 0; i < this.baristaCount; i++) {
      this.createBarista();
    }
  }

  createBarista() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.barista);
    container.addChild(sprite);
    container.x = Math.random() * this.app.screen.width;
    container.y = Math.random() * this.app.screen.height;
    container.state = 'idle';
    container.targetX = container.x;
    container.targetY = container.y;
    container.assignedCustomer = null;
    container.assignedMachine = null;
    
    // Add effects
    this.effects.createShadow(container, sprite, { offsetY: 5 });
    this.effects.idleAnimation(container);
    
    this.baristas.addChild(container);
    this.effects.spawnAnimation(container);
  }

  spawnCustomer() {
    const availableCounter = this.counters.children.find(counter => !counter.customer);
    if (availableCounter) {
      const container = new PIXI.Container();
      const sprite = this.getSprite(SPRITES.customer);
      container.addChild(sprite);
      container.x = availableCounter.x;
      container.y = availableCounter.y;
      container.counter = availableCounter;
      availableCounter.customer = container;
      
      // Add effects
      this.effects.createShadow(container, sprite, { offsetY: 5 });
      this.customers.addChild(container);
      this.effects.spawnAnimation(container);
    }
  }

  moveBarista(barista, targetX, targetY, elapsedSecs) {
    const dx = targetX - barista.x;
    const dy = targetY - barista.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance > 1) {
      const moveDistance = this.baristaSpeed * elapsedSecs;
      const ratio = moveDistance / distance;
      barista.x += dx * ratio;
      barista.y += dy * ratio;
      
      // Add movement particles
      if (Math.random() < 0.3) {
        this.effects.createParticleSystem(barista, {
          maxParticles: 2,
          spawnInterval: 0.1,
          radius: 10
        });
      }
      return false;
    }
    return true;
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    // Spawn customers
    this.customerSpawnTimer += elapsedSecs;
    if (this.customerSpawnTimer >= this.customerSpawnTime) {
      this.spawnCustomer();
      this.customerSpawnTimer = 0;
    }

    // Update baristas
    this.baristas.children.forEach(barista => {
      switch (barista.state) {
        case 'idle':
          const customer = this.customers.children.find(c => !c.beingServed);
          if (customer) {
            barista.state = 'moving_to_customer';
            barista.assignedCustomer = customer;
            customer.beingServed = true;
          }
          break;

        case 'moving_to_customer':
          if (this.moveBarista(barista, barista.assignedCustomer.x, barista.assignedCustomer.y, elapsedSecs)) {
            barista.state = 'moving_to_machine';
            const machine = this.coffeeMachines.children.find(m => !m.inUse);
            barista.assignedMachine = machine;
            machine.inUse = true;
          }
          break;

        case 'moving_to_machine':
          if (this.moveBarista(barista, barista.assignedMachine.x, barista.assignedMachine.y, elapsedSecs)) {
            barista.state = 'making_coffee';
            barista.coffeeTimer = 0;
            // Start coffee making effects
            this.effects.createSpiralParticles(barista.assignedMachine, {
              y: -30,
              color: 0x8B4513
            });
          }
          break;

        case 'making_coffee':
          barista.coffeeTimer += elapsedSecs;
          if (barista.coffeeTimer >= this.coffeeMachineTime) {
            barista.state = 'serving_customer';
            // Coffee ready effect
            this.effects.createImpactEffect(barista.assignedMachine, {
              y: -20,
              color: 0x8B4513
            });
          }
          break;

        case 'serving_customer':
          if (this.moveBarista(barista, barista.assignedCustomer.x, barista.assignedCustomer.y, elapsedSecs)) {
            // Complete order effects
            this.effects.showFloatingText(barista.assignedCustomer, `+$${this.coffeePrice}`);
            this.effects.createExplosionParticles(barista.assignedCustomer, {
              color: 0xFFD700,
              count: 20
            });
            
            this.money += this.coffeePrice;
            this.customers.removeChild(barista.assignedCustomer);
            barista.assignedCustomer.counter.customer = null;
            barista.assignedMachine.inUse = false;
            barista.state = 'idle';
            barista.assignedCustomer = null;
            barista.assignedMachine = null;
          }
          break;
      }
    });
  }

  getSprite(spriteConfig) {
    const texture = PIXI.Texture.from(spriteConfig.path);
    const sprite = new PIXI.Sprite(texture);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    sprite.anchor.set(0.5);
    return sprite;
  }

  upgradeBaristaCount() {
    if (this.money >= this.baristaCountCost) {
      this.money -= this.baristaCountCost;
      this.baristaCount++;
      this.createBarista();
      this.baristaCountCost *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 5 });
    }
  }

  upgradeBaristaSpeed() {
    if (this.money >= this.baristaSpeedCost) {
      this.money -= this.baristaSpeedCost;
      this.baristaSpeed *= 1.2;
      this.baristaSpeedCost *= 2;
      this.baristas.children.forEach(barista => {
        this.effects.highlightCharacter(barista.children[0], { color: 0x00FF00 });
      });
    }
  }

  upgradeCoffeeMachine() {
    if (this.money >= this.coffeeMachineCost) {
      this.money -= this.coffeeMachineCost;
      this.coffeeMachineTime *= 0.8;
      this.coffeeMachineCost *= 2;
      this.coffeeMachines.children.forEach(machine => {
        this.effects.createExplosionParticles(machine, {
          color: 0x00FF00,
          count: 30
        });
      });
    }
  }

  upgradeCounterCount() {
    if (this.money >= this.counterCountCost) {
      this.money -= this.counterCountCost;
      this.counterCount++;
      const i = this.counterCount - 1;
      
      const counterContainer = new PIXI.Container();
      const counter = this.getSprite(SPRITES.counter);
      counterContainer.addChild(counter);
      counterContainer.x = STATION_POSITIONS.COUNTER_START_X + (i * STATION_POSITIONS.COUNTER_SPACING);
      counterContainer.y = STATION_POSITIONS.COUNTER_Y;
      counterContainer.customer = null;
      this.counters.addChild(counterContainer);

      const machineContainer = new PIXI.Container();
      const machine = this.getSprite(SPRITES.coffeeMachine);
      machineContainer.addChild(machine);
      machineContainer.x = STATION_POSITIONS.MACHINE_START_X + (i * STATION_POSITIONS.MACHINE_SPACING);
      machineContainer.y = STATION_POSITIONS.MACHINE_Y;
      machineContainer.inUse = false;
      this.coffeeMachines.addChild(machineContainer);

      this.effects.createShadow(counterContainer, counter, { offsetY: 10 });
      this.effects.createShadow(machineContainer, machine, { offsetY: 5 });
      
      this.effects.spawnAnimation(counterContainer);
      this.effects.spawnAnimation(machineContainer);
      
      this.counterCountCost *= 2;
    }
  }

  upgradeCoffeePrice() {
    if (this.money >= this.coffeePriceCost) {
      this.money -= this.coffeePriceCost;
      this.coffeePrice *= 1.2;
      this.coffeePriceCost *= 2;
      this.effects.createExplosionParticles(this.app.stage, {
        x: this.app.screen.width / 2,
        y: this.app.screen.height / 2,
        color: 0xFFD700,
        count: 50
      });
    }
  }

  upgradeCustomerAttraction() {
    if (this.money >= this.customerAttractionCost) {
      this.money -= this.customerAttractionCost;
      this.customerSpawnTime *= 0.8;
      this.customerAttractionCost *= 2;
      this.effects.createSpiralParticles(this.app.stage, {
        x: this.app.screen.width / 2,
        y: this.app.screen.height / 2,
        color: 0xFF69B4
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
