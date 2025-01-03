import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, POSITIONS } from './gameData';
import { SPRITES } from './assetManifest';
import { loadAssets } from './utils';

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

    // Initialize properties
    this.ready = false;
    this.money = INITIAL_VALUES.MONEY;
    this.baristaCount = INITIAL_VALUES.BARISTA_COUNT;
    this.baristaSpeed = INITIAL_VALUES.BARISTA_SPEED;
    this.customerCapacity = INITIAL_VALUES.CUSTOMER_CAPACITY;
    this.coffeePrice = INITIAL_VALUES.COFFEE_PRICE;
    this.processingSpeed = INITIAL_VALUES.PROCESSING_SPEED;

    this.baristaCost = UPGRADE_COSTS.BARISTA;
    this.baristaSpeedCost = UPGRADE_COSTS.BARISTA_SPEED;
    this.customerCapacityCost = UPGRADE_COSTS.CUSTOMER_CAPACITY;
    this.coffeePriceCost = UPGRADE_COSTS.COFFEE_PRICE;
    this.processingSpeedCost = UPGRADE_COSTS.PROCESSING_SPEED;

    this.customerSpawnTimer = 0;
    this.lastTimestamp = performance.now();

    // Initialize containers
    this.customers = new PIXI.Container();
    this.baristas = new PIXI.Container();

    // Load textures first
    this.textures = {};
    const loader = PIXI.Loader.shared;
    Object.entries(SPRITES).forEach(([key, sprite]) => {
      loader.add(key, sprite.path);
    });

    loader.load((loader, resources) => {
      Object.keys(SPRITES).forEach(key => {
        this.textures[key] = resources[key].texture;
      });
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(spriteConfig) {
    const sprite = new PIXI.Sprite(this.textures[spriteConfig.path]);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite(SPRITES.background);
    this.counter = this.getSprite(SPRITES.counter);
    this.coffeeStation = this.getSprite(SPRITES.coffee_station);
    this.pickup = this.getSprite(SPRITES.pickup);

    this.counter.position.set(POSITIONS.COUNTER.x, POSITIONS.COUNTER.y);
    this.coffeeStation.position.set(POSITIONS.COFFEE_STATION.x, POSITIONS.COFFEE_STATION.y);
    this.pickup.position.set(POSITIONS.PICKUP.x, POSITIONS.PICKUP.y);

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.counter);
    this.app.stage.addChild(this.coffeeStation);
    this.app.stage.addChild(this.pickup);
    this.app.stage.addChild(this.customers);
    this.app.stage.addChild(this.baristas);

    for (let i = 0; i < this.baristaCount; i++) {
      this.createBarista();
    }
  }

  createCustomer() {
    const customer = this.getSprite(SPRITES.customer);
    customer.anchor.set(0.5);
    customer.position.set(POSITIONS.ENTRANCE.x, POSITIONS.ENTRANCE.y);
    customer.state = 'moving_to_counter';
    customer.orderStatus = new PIXI.Text('Moving to counter...', {
      fontSize: 12,
      fill: 0xFFFFFF
    });
    customer.orderStatus.anchor.set(0.5, 1);
    customer.orderStatus.position.set(customer.width/2, -10);
    customer.addChild(customer.orderStatus);
    this.customers.addChild(customer);
  }

  createBarista() {
    const barista = this.getSprite(SPRITES.barista);
    barista.anchor.set(0.5);
    barista.position.set(POSITIONS.COUNTER.x, POSITIONS.COUNTER.y);
    barista.state = 'idle';
    barista.assignedCustomer = null;
    this.baristas.addChild(barista);
  }

  moveTowards(entity, target, speed, elapsedSecs) {
    const dx = target.x - entity.x;
    const dy = target.y - entity.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance < 2) return true;

    const moveSpeed = speed * elapsedSecs;
    entity.x += (dx / distance) * moveSpeed;
    entity.y += (dy / distance) * moveSpeed;
    return false;
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.customerSpawnTimer += elapsedSecs;
    if (this.customerSpawnTimer >= INITIAL_VALUES.CUSTOMER_SPAWN_RATE && 
        this.customers.children.length < this.customerCapacity) {
      this.createCustomer();
      this.customerSpawnTimer = 0;
    }

    this.customers.children.forEach(customer => {
      switch (customer.state) {
        case 'moving_to_counter':
          if (this.moveTowards(customer, POSITIONS.COUNTER, 100 * this.baristaSpeed, elapsedSecs)) {
            customer.state = 'waiting_for_barista';
            customer.orderStatus.text = 'Waiting for barista...';
          }
          break;
        case 'moving_to_pickup':
          if (this.moveTowards(customer, POSITIONS.PICKUP, 100 * this.baristaSpeed, elapsedSecs)) {
            customer.state = 'collecting';
            customer.orderStatus.text = 'Collecting coffee...';
            setTimeout(() => {
              customer.state = 'leaving';
              customer.orderStatus.text = 'Thank you!';
              this.money += this.coffeePrice;
            }, 1000 / this.processingSpeed);
          }
          break;
        case 'leaving':
          if (this.moveTowards(customer, POSITIONS.EXIT, 100 * this.baristaSpeed, elapsedSecs)) {
            this.customers.removeChild(customer);
          }
          break;
      }
    });

    this.baristas.children.forEach(barista => {
      switch (barista.state) {
        case 'idle':
          const waitingCustomer = this.customers.children.find(c => 
            c.state === 'waiting_for_barista' && !this.baristas.children.some(b => 
              b.assignedCustomer === c));
          if (waitingCustomer) {
            barista.assignedCustomer = waitingCustomer;
            barista.state = 'moving_to_station';
            waitingCustomer.orderStatus.text = 'Order taken...';
          }
          break;
        case 'moving_to_station':
          if (this.moveTowards(barista, POSITIONS.COFFEE_STATION, 150 * this.baristaSpeed, elapsedSecs)) {
            barista.state = 'making_coffee';
            barista.coffeeTimer = 0;
          }
          break;
        case 'making_coffee':
          barista.coffeeTimer += elapsedSecs * this.processingSpeed;
          if (barista.coffeeTimer >= INITIAL_VALUES.COFFEE_MAKE_TIME) {
            barista.state = 'moving_to_pickup';
          }
          break;
        case 'moving_to_pickup':
          if (this.moveTowards(barista, POSITIONS.PICKUP, 150 * this.baristaSpeed, elapsedSecs)) {
            if (barista.assignedCustomer) {
              barista.assignedCustomer.state = 'moving_to_pickup';
            }
            barista.state = 'returning';
          }
          break;
        case 'returning':
          if (this.moveTowards(barista, POSITIONS.COUNTER, 150 * this.baristaSpeed, elapsedSecs)) {
            barista.state = 'idle';
            barista.assignedCustomer = null;
          }
          break;
      }
    });
  }

  upgradeBarista() {
    if (this.money >= this.baristaCost) {
      this.money -= this.baristaCost;
      this.baristaCount++;
      this.createBarista();
      this.baristaCost *= 2;
    }
  }

  upgradeBaristaSpeed() {
    if (this.money >= this.baristaSpeedCost) {
      this.money -= this.baristaSpeedCost;
      this.baristaSpeed *= 1.2;
      this.baristaSpeedCost *= 2;
    }
  }

  upgradeCustomerCapacity() {
    if (this.money >= this.customerCapacityCost) {
      this.money -= this.customerCapacityCost;
      this.customerCapacity++;
      this.customerCapacityCost *= 2;
    }
  }

  upgradeCoffeePrice() {
    if (this.money >= this.coffeePriceCost) {
      this.money -= this.coffeePriceCost;
      this.coffeePrice = Math.floor(this.coffeePrice * 1.2);
      this.coffeePriceCost *= 2;
    }
  }

  upgradeProcessingSpeed() {
    if (this.money >= this.processingSpeedCost) {
      this.money -= this.processingSpeedCost;
      this.processingSpeed *= 1.2;
      this.processingSpeedCost *= 2;
    }
  }

  destroy() {
    this.app.destroy(true);
  }
}
