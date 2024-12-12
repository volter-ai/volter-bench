import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, POSITIONS } from './gameData';
import { SPRITES } from './assetManifest';
import { loadAssets } from './utils'

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
    this.money = INITIAL_VALUES.MONEY;
    this.baristaCount = INITIAL_VALUES.BARISTA_COUNT;
    this.baristaSpeed = INITIAL_VALUES.BARISTA_SPEED;
    this.coffeeEfficiency = INITIAL_VALUES.COFFEE_EFFICIENCY;
    this.customerCapacity = INITIAL_VALUES.CUSTOMER_CAPACITY;
    this.coffeePrice = INITIAL_VALUES.COFFEE_PRICE;
    
    this.customerSpawnTimer = 0;
    this.lastTimestamp = performance.now();

    this.upgradeCosts = {
      barista: UPGRADE_COSTS.BARISTA,
      baristaSpeed: UPGRADE_COSTS.BARISTA_SPEED,
      coffeeEfficiency: UPGRADE_COSTS.COFFEE_EFFICIENCY,
      customerCapacity: UPGRADE_COSTS.CUSTOMER_CAPACITY,
      coffeePrice: UPGRADE_COSTS.COFFEE_PRICE
    };

    // Initialize textures before loading
    this.textures = {};
    
    // Load all textures first
    Object.entries(SPRITES).forEach(([key, sprite]) => {
      this.textures[key] = PIXI.Texture.from(sprite.path);
    });

    // Then create game objects
    this.createGameObjects();
    this.app.ticker.add(this.gameLoop.bind(this));
    this.ready = true;
  }

  getSprite(spriteConfig) {
    const sprite = new PIXI.Sprite(this.textures[spriteConfig.path]);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    sprite.anchor.set(0.5);
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite(SPRITES.background);
    this.customers = new PIXI.Container();
    this.baristas = new PIXI.Container();
    
    // Create initial barista
    this.createBarista();

    // Create static objects
    this.counter = this.getSprite(SPRITES.counter);
    this.counter.position.set(POSITIONS.COUNTER.x, POSITIONS.COUNTER.y);
    
    this.coffeeStation = this.getSprite(SPRITES.coffee_station);
    this.coffeeStation.position.set(POSITIONS.COFFEE_STATION.x, POSITIONS.COFFEE_STATION.y);

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.counter);
    this.app.stage.addChild(this.coffeeStation);
    this.app.stage.addChild(this.customers);
    this.app.stage.addChild(this.baristas);
  }

  createCustomer() {
    const customer = this.getSprite(SPRITES.customer);
    customer.position.set(POSITIONS.ENTRANCE.x, POSITIONS.ENTRANCE.y);
    customer.state = 'entering';
    customer.orderTime = 0;
    this.customers.addChild(customer);
  }

  createBarista() {
    const barista = this.getSprite(SPRITES.barista);
    barista.position.set(POSITIONS.COUNTER.x, POSITIONS.COUNTER.y);
    barista.state = 'idle';
    barista.orderTime = 0;
    this.baristas.addChild(barista);
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    // Spawn customers
    this.customerSpawnTimer += elapsedSecs;
    if (this.customerSpawnTimer >= INITIAL_VALUES.CUSTOMER_SPAWN_RATE && 
        this.customers.children.length < this.customerCapacity) {
      this.createCustomer();
      this.customerSpawnTimer = 0;
    }

    // Update customers
    this.customers.children.forEach(customer => {
      if (customer.state === 'entering') {
        customer.position.set(POSITIONS.COUNTER.x, POSITIONS.COUNTER.y);
        customer.state = 'ordering';
      }
    });

    // Update baristas
    this.baristas.children.forEach(barista => {
      if (barista.state === 'idle') {
        const orderingCustomer = this.customers.children.find(c => c.state === 'ordering');
        if (orderingCustomer) {
          barista.state = 'preparing';
          barista.orderTime = 0;
          orderingCustomer.state = 'waiting';
          orderingCustomer.position.set(POSITIONS.PICKUP.x, POSITIONS.PICKUP.y);
        }
      } else if (barista.state === 'preparing') {
        barista.orderTime += elapsedSecs * this.baristaSpeed * this.coffeeEfficiency;
        if (barista.orderTime >= INITIAL_VALUES.COFFEE_PREP_TIME) {
          const waitingCustomer = this.customers.children.find(c => c.state === 'waiting');
          if (waitingCustomer) {
            this.money += this.coffeePrice;
            this.customers.removeChild(waitingCustomer);
          }
          barista.state = 'idle';
        }
      }
    });
  }

  upgradeBarista() {
    if (this.money >= this.upgradeCosts.barista) {
      this.money -= this.upgradeCosts.barista;
      this.createBarista();
      this.upgradeCosts.barista *= 2;
    }
  }

  upgradeBaristaSpeed() {
    if (this.money >= this.upgradeCosts.baristaSpeed) {
      this.money -= this.upgradeCosts.baristaSpeed;
      this.baristaSpeed *= 1.2;
      this.upgradeCosts.baristaSpeed *= 2;
    }
  }

  upgradeCoffeeEfficiency() {
    if (this.money >= this.upgradeCosts.coffeeEfficiency) {
      this.money -= this.upgradeCosts.coffeeEfficiency;
      this.coffeeEfficiency *= 1.2;
      this.upgradeCosts.coffeeEfficiency *= 2;
    }
  }

  upgradeCustomerCapacity() {
    if (this.money >= this.upgradeCosts.customerCapacity) {
      this.money -= this.upgradeCosts.customerCapacity;
      this.customerCapacity += 1;
      this.upgradeCosts.customerCapacity *= 2;
    }
  }

  upgradeCoffeePrice() {
    if (this.money >= this.upgradeCosts.coffeePrice) {
      this.money -= this.upgradeCosts.coffeePrice;
      this.coffeePrice += 2;
      this.upgradeCosts.coffeePrice *= 2;
    }
  }

  destroy() {
    this.app.destroy(true);
  }
}
