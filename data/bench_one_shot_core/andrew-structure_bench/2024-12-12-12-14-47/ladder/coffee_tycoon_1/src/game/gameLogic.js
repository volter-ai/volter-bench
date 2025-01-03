import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, GAME_CONFIG } from './gameData';
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
    
    // Initialize effects library
    this.effects = new EffectsLibrary(this.app);

    this.ready = false;
    this.money = INITIAL_VALUES.MONEY;
    this.baristaCount = INITIAL_VALUES.BARISTA_COUNT;
    this.baristaSpeed = INITIAL_VALUES.BARISTA_SPEED;
    this.brewTime = INITIAL_VALUES.COFFEE_BREW_TIME;
    this.maxCustomers = INITIAL_VALUES.MAX_CUSTOMERS;
    this.coffeePrice = INITIAL_VALUES.COFFEE_PRICE;
    
    this.baristaCost = UPGRADE_COSTS.BARISTA;
    this.baristaSpeedCost = UPGRADE_COSTS.BARISTA_SPEED;
    this.brewSpeedCost = UPGRADE_COSTS.BREW_SPEED;
    this.maxCustomersCost = UPGRADE_COSTS.MAX_CUSTOMERS;
    this.priceCost = UPGRADE_COSTS.PRICE_MULTIPLIER;

    this.customerSpawnTimer = 0;

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
    
    this.baristas = new PIXI.Container();
    this.customers = new PIXI.Container();
    this.coffeeMachines = new PIXI.Container();

    // Create initial barista
    this.createBarista();

    // Create coffee machines
    for(let i = 0; i < 3; i++) {
      this.createCoffeeMachine(100 + i * 100, 100);
    }

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.coffeeMachines);
    this.app.stage.addChild(this.customers);
    this.app.stage.addChild(this.baristas);
  }

  createBarista() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.barista);
    sprite.anchor.set(0.5);
    
    // Add shadow
    this.effects.createShadow(container, sprite);
    
    container.addChild(sprite);
    container.x = 400;
    container.y = 300;
    container.busy = false;
    container.targetX = container.x;
    container.targetY = container.y;
    container.task = null;
    container.sprite = sprite;

    // Add idle animation
    this.effects.idleAnimation(sprite);
    
    this.baristas.addChild(container);
  }

  createCustomer() {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.customer);
    sprite.anchor.set(0.5);
    
    // Add shadow
    this.effects.createShadow(container, sprite);
    
    container.addChild(sprite);
    container.x = 50;
    container.y = 500;
    container.waiting = true;
    container.hasOrder = false;
    container.destroyed = false;
    container.sprite = sprite;
    
    this.customers.addChild(container);
    
    // Spawn animation
    this.effects.spawnAnimation(container);
  }

  createCoffeeMachine(x, y) {
    const container = new PIXI.Container();
    const sprite = this.getSprite(SPRITES.coffeeMachine);
    sprite.anchor.set(0.5);
    
    container.addChild(sprite);
    container.x = x;
    container.y = y;
    container.brewing = false;
    container.progress = 0;
    container.sprite = sprite;
    
    this.coffeeMachines.addChild(container);
  }

  gameLoop(delta) {
    if (!this.ready) return;
    
    const elapsedSecs = delta / 60;

    // Spawn customers
    this.customerSpawnTimer += elapsedSecs;
    if (this.customerSpawnTimer >= GAME_CONFIG.CUSTOMER_SPAWN_TIME) {
      if (this.customers.children.length < this.maxCustomers) {
        this.createCustomer();
      }
      this.customerSpawnTimer = 0;
    }

    // Update coffee machines
    this.coffeeMachines.children.forEach(machine => {
      if (machine.brewing) {
        machine.progress += elapsedSecs / this.brewTime;
        
        // Create brewing particles
        if (Math.random() < 0.1) {
          this.effects.createSpiralParticles(this.app.stage, {
            x: machine.x,
            y: machine.y - 30,
            count: 10
          });
        }
        
        if (machine.progress >= 1) {
          machine.brewing = false;
          machine.progress = 0;
          // Create completion effect
          this.effects.createImpactEffect(this.app.stage, {
            x: machine.x,
            y: machine.y,
            color: 0x7FFFD4
          });
        }
      }
    });

    // Update baristas
    this.baristas.children.forEach(barista => {
      if (!barista.busy) {
        // Find waiting customer
        const customer = this.customers.children.find(c => c.waiting && !c.hasOrder && !c.destroyed);
        if (customer) {
          // Find free coffee machine
          const machine = this.coffeeMachines.children.find(m => !m.brewing);
          if (machine) {
            barista.busy = true;
            machine.brewing = true;
            customer.hasOrder = true;
            
            // Highlight barista starting task
            this.effects.highlightCharacter(barista.sprite);
            
            // Create task for barista
            barista.task = {
              type: 'brew',
              machine: machine,
              customer: customer,
              progress: 0,
              totalTime: this.brewTime
            };
          }
        }
      } else if (barista.task) {
        // Handle ongoing tasks
        switch(barista.task.type) {
          case 'brew':
            barista.task.progress += elapsedSecs;
            if (barista.task.progress >= barista.task.totalTime) {
              barista.task.type = 'deliver';
              barista.task.progress = 0;
              barista.task.totalTime = 1 / this.baristaSpeed;
              
              // Effect when coffee is ready
              this.effects.createImpactEffect(this.app.stage, {
                x: barista.task.machine.x,
                y: barista.task.machine.y,
                color: 0xFFFFFF
              });
            }
            break;
          case 'deliver':
            barista.task.progress += elapsedSecs;
            if (barista.task.progress >= barista.task.totalTime) {
              if (!barista.task.customer.destroyed) {
                this.money += this.coffeePrice;
                barista.task.customer.destroyed = true;
                
                // Show floating money text
                this.effects.showFloatingText(barista.task.customer, `+$${this.coffeePrice}`);
                
                // Customer satisfaction effect
                this.effects.createExplosionParticles(this.app.stage, {
                  x: barista.task.customer.x,
                  y: barista.task.customer.y,
                  color: 0xFFD700
                });
                
                this.customers.removeChild(barista.task.customer);
              }
              barista.busy = false;
              barista.task = null;
            }
            break;
        }
      }
    });
  }

  upgradeBarista() {
    if (this.money >= this.baristaCost) {
      this.money -= this.baristaCost;
      this.createBarista();
      this.baristaCost *= GAME_CONFIG.COST_MULTIPLIER;
      
      // Upgrade effects
      this.effects.screenShake(this.app.stage);
      this.effects.createExplosionParticles(this.app.stage, {
        x: SCREEN_SIZE.width/2,
        y: SCREEN_SIZE.height/2,
        color: 0x00FF00
      });
    }
  }

  upgradeBaristaSpeed() {
    if (this.money >= this.baristaSpeedCost) {
      this.money -= this.baristaSpeedCost;
      this.baristaSpeed *= 1.2;
      this.baristaSpeedCost *= GAME_CONFIG.COST_MULTIPLIER;
      
      // Upgrade effects
      this.baristas.children.forEach(barista => {
        this.effects.flashColor(barista.sprite, {color: 0x00FF00});
      });
    }
  }

  upgradeBrewSpeed() {
    if (this.money >= this.brewSpeedCost) {
      this.money -= this.brewSpeedCost;
      this.brewTime *= 0.8;
      this.brewSpeedCost *= GAME_CONFIG.COST_MULTIPLIER;
      
      // Upgrade effects
      this.coffeeMachines.children.forEach(machine => {
        this.effects.flashColor(machine.sprite, {color: 0x00FF00});
      });
    }
  }

  upgradeMaxCustomers() {
    if (this.money >= this.maxCustomersCost) {
      this.money -= this.maxCustomersCost;
      this.maxCustomers += 1;
      this.maxCustomersCost *= GAME_CONFIG.COST_MULTIPLIER;
      
      // Upgrade effects
      this.effects.createExplosionParticles(this.app.stage, {
        x: 50,
        y: 500,
        color: 0x00FF00
      });
    }
  }

  upgradeCoffeePrice() {
    if (this.money >= this.priceCost) {
      this.money -= this.priceCost;
      this.coffeePrice *= 1.2;
      this.priceCost *= GAME_CONFIG.COST_MULTIPLIER;
      
      // Upgrade effects
      this.effects.showFloatingText(this.app.stage, `Price Up!`, {
        x: SCREEN_SIZE.width/2,
        y: SCREEN_SIZE.height/2,
        color: 0xFFD700
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
