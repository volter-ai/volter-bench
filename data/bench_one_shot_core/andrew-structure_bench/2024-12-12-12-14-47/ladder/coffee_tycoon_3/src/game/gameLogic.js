import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, LOCATIONS } from './gameData';
import { SPRITES } from './assetManifest';
import { loadAssets } from './utils';
import { EffectsLibrary } from '../lib/effectsLib';

const SCREEN_SIZE = {
  width: 800,
  height: 600
};

class BaristaContainer extends PIXI.Container {
  constructor(sprite, effects) {
    super();
    this.sprite = sprite;
    this.sprite.anchor.set(0.5);
    this.addChild(this.sprite);
    
    // Add shadow
    this.shadow = effects.createShadow(this, sprite, {
      offsetY: 5,
      alpha: 0.2
    });
    
    // Add idle animation to shadow
    effects.idleAnimation(this.shadow);
  }
}

class CustomerContainer extends PIXI.Container {
  constructor(sprite, effects) {
    super();
    this.sprite = sprite;
    this.sprite.anchor.set(0.5);
    this.addChild(this.sprite);
    
    // Add shadow
    this.shadow = effects.createShadow(this, sprite, {
      offsetY: 5,
      alpha: 0.2
    });
    
    // Add idle animation to shadow
    effects.idleAnimation(this.shadow);
  }
}

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
    this.money = 0;
    this.coffeePrice = INITIAL_VALUES.COFFEE_PRICE;
    this.coffeeMakeSpeed = INITIAL_VALUES.COFFEE_MAKE_SPEED;
    this.baristaCount = INITIAL_VALUES.BARISTA_COUNT;
    this.customerCapacity = INITIAL_VALUES.CUSTOMER_CAPACITY;
    this.baristaEfficiency = INITIAL_VALUES.BARISTA_EFFICIENCY;

    this.coffeePriceCost = UPGRADE_COSTS.COFFEE_PRICE;
    this.coffeeSpeedCost = UPGRADE_COSTS.COFFEE_SPEED;
    this.baristaCountCost = UPGRADE_COSTS.BARISTA_COUNT;
    this.customerCapacityCost = UPGRADE_COSTS.CUSTOMER_CAPACITY;
    this.baristaEfficiencyCost = UPGRADE_COSTS.BARISTA_EFFICIENCY;

    if (!PIXI.Loader.shared.resources) {
      PIXI.Loader.shared.destroy();
      PIXI.Loader.shared = new PIXI.Loader();
    }

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(spriteConfig) {
    const key = Object.entries(SPRITES).find(([k, s]) => s.path === spriteConfig.path)[0];
    const texture = PIXI.Loader.shared.resources[key].texture;
    const sprite = new PIXI.Sprite(texture);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite(SPRITES.background);
    this.app.stage.addChild(this.background);

    this.stations = new PIXI.Container();
    this.baristas = new PIXI.Container();
    this.customers = new PIXI.Container();
    
    LOCATIONS.COFFEE_STATIONS.forEach(pos => {
      const station = this.getSprite(SPRITES.coffee_station);
      station.x = pos.x;
      station.y = pos.y;
      station.anchor.set(0.5);
      this.stations.addChild(station);
    });

    const counter = this.getSprite(SPRITES.counter);
    counter.x = LOCATIONS.COUNTER.x;
    counter.y = LOCATIONS.COUNTER.y;
    counter.anchor.set(0.5);

    const register = this.getSprite(SPRITES.register);
    register.x = LOCATIONS.REGISTER.x;
    register.y = LOCATIONS.REGISTER.y;
    register.anchor.set(0.5);

    for (let i = 0; i < this.baristaCount; i++) {
      this.createBarista();
    }

    this.app.stage.addChild(this.stations);
    this.app.stage.addChild(counter);
    this.app.stage.addChild(register);
    this.app.stage.addChild(this.baristas);
    this.app.stage.addChild(this.customers);

    this.lastTimestamp = performance.now();
    this.customerSpawnTimer = 0;
  }

  createBarista() {
    const sprite = this.getSprite(SPRITES.barista);
    const baristaContainer = new BaristaContainer(sprite, this.effects);
    const station = LOCATIONS.COFFEE_STATIONS[this.baristas.children.length % LOCATIONS.COFFEE_STATIONS.length];
    baristaContainer.x = station.x;
    baristaContainer.y = station.y;
    baristaContainer.state = 'making';
    baristaContainer.coffeeTimer = 0;
    baristaContainer.coffees = 0;
    
    // Spawn animation
    this.effects.spawnAnimation(baristaContainer);
    
    this.baristas.addChild(baristaContainer);
  }

  createCustomer() {
    if (this.customers.children.length >= this.customerCapacity) return;
    
    const sprite = this.getSprite(SPRITES.customer);
    const customerContainer = new CustomerContainer(sprite, this.effects);
    customerContainer.x = LOCATIONS.ENTRANCE.x;
    customerContainer.y = LOCATIONS.ENTRANCE.y;
    customerContainer.state = 'moving_to_counter';
    
    // Spawn animation
    this.effects.spawnAnimation(customerContainer);
    
    this.customers.addChild(customerContainer);
  }

  moveTowards(entity, target, speed, elapsedSecs) {
    const dx = target.x - entity.x;
    const dy = target.y - entity.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance < 5) return true;

    const moveDistance = speed * elapsedSecs;
    const ratio = moveDistance / distance;
    
    entity.x += dx * ratio;
    entity.y += dy * ratio;
    
    return false;
  }

  gameLoop(delta) {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.customerSpawnTimer += elapsedSecs;
    if (this.customerSpawnTimer >= 1) {
      this.createCustomer();
      this.customerSpawnTimer = 0;
    }

    this.baristas.children.forEach(barista => {
      switch (barista.state) {
        case 'making':
          barista.coffeeTimer += elapsedSecs;
          if (barista.coffeeTimer >= this.coffeeMakeSpeed) {
            barista.coffeeTimer = 0;
            barista.coffees = this.baristaEfficiency;
            barista.state = 'delivering';
            
            // Coffee completion effect
            this.effects.createSpiralParticles(this.app.stage, {
              x: barista.x,
              y: barista.y - 30
            });
            this.effects.flashColor(barista.sprite, {
              color: 0x7FFFD4
            });
          } else {
            // Making coffee particles
            if (Math.random() < 0.1) {
              this.effects.createSpiralParticles(this.app.stage, {
                x: barista.x,
                y: barista.y - 30,
                count: 5
              });
            }
          }
          break;
        case 'delivering':
          if (this.moveTowards(barista, LOCATIONS.COUNTER, INITIAL_VALUES.BARISTA_SPEED, elapsedSecs)) {
            barista.coffees = 0;
            barista.state = 'returning';
          }
          break;
        case 'returning':
          const station = LOCATIONS.COFFEE_STATIONS[this.baristas.children.indexOf(barista) % LOCATIONS.COFFEE_STATIONS.length];
          if (this.moveTowards(barista, station, INITIAL_VALUES.BARISTA_SPEED, elapsedSecs)) {
            barista.state = 'making';
          }
          break;
      }
    });

    this.customers.children.forEach(customer => {
      switch (customer.state) {
        case 'moving_to_counter':
          if (this.moveTowards(customer, LOCATIONS.COUNTER, INITIAL_VALUES.CUSTOMER_SPEED, elapsedSecs)) {
            customer.state = 'moving_to_register';
          }
          break;
        case 'moving_to_register':
          if (this.moveTowards(customer, LOCATIONS.REGISTER, INITIAL_VALUES.CUSTOMER_SPEED, elapsedSecs)) {
            this.money += this.coffeePrice;
            customer.state = 'leaving';
            
            // Purchase effects
            this.effects.showFloatingText(customer, `+$${this.coffeePrice}`);
            this.effects.createExplosionParticles(this.app.stage, {
              x: LOCATIONS.REGISTER.x,
              y: LOCATIONS.REGISTER.y,
              color: 0xFFD700
            });
          }
          break;
        case 'leaving':
          if (this.moveTowards(customer, LOCATIONS.EXIT, INITIAL_VALUES.CUSTOMER_SPEED, elapsedSecs)) {
            this.customers.removeChild(customer);
          }
          break;
      }
    });
  }

  upgradeCoffeePrice() {
    if (this.money >= this.coffeePriceCost) {
      this.money -= this.coffeePriceCost;
      this.coffeePrice *= 1.5;
      this.coffeePriceCost *= 2;
      
      // Upgrade effect
      const register = this.app.stage.children.find(child => 
        child.texture === PIXI.Loader.shared.resources.register.texture
      );
      this.effects.flashColor(register, { color: 0xFFD700 });
      this.effects.createExplosionParticles(this.app.stage, {
        x: LOCATIONS.REGISTER.x,
        y: LOCATIONS.REGISTER.y,
        color: 0xFFD700
      });
    }
  }

  upgradeCoffeeSpeed() {
    if (this.money >= this.coffeeSpeedCost) {
      this.money -= this.coffeeSpeedCost;
      this.coffeeMakeSpeed *= 0.8;
      this.coffeeSpeedCost *= 2;
      
      // Upgrade effect
      LOCATIONS.COFFEE_STATIONS.forEach(station => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: station.x,
          y: station.y,
          count: 30
        });
      });
    }
  }

  upgradeBaristaCount() {
    if (this.money >= this.baristaCountCost) {
      this.money -= this.baristaCountCost;
      this.baristaCount++;
      this.createBarista();
      this.baristaCountCost *= 2;
    }
  }

  upgradeCustomerCapacity() {
    if (this.money >= this.customerCapacityCost) {
      this.money -= this.customerCapacityCost;
      this.customerCapacity++;
      this.customerCapacityCost *= 2;
      
      // Upgrade effect
      this.effects.createExplosionParticles(this.app.stage, {
        x: LOCATIONS.ENTRANCE.x,
        y: LOCATIONS.ENTRANCE.y,
        color: 0x00FF00
      });
    }
  }

  upgradeBaristaEfficiency() {
    if (this.money >= this.baristaEfficiencyCost) {
      this.money -= this.baristaEfficiencyCost;
      this.baristaEfficiency++;
      this.baristaEfficiencyCost *= 2;
      
      // Upgrade effect
      this.baristas.children.forEach(barista => {
        this.effects.highlightCharacter(barista.sprite);
        this.effects.createSpiralParticles(this.app.stage, {
          x: barista.x,
          y: barista.y,
          count: 20,
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
