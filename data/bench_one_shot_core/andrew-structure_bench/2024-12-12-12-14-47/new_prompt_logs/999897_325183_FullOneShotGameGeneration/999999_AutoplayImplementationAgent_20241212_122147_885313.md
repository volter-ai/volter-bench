Role: system
Content: You are an expert software developer. Your job is to implement the 'autoplay' AI features in the `src/GameAI.js` file

Here is a sample implementation from another game

```js src/GameAI.js
import { AIUtils } from './AIUtils';

const UPGRADES = [
  'DIFFICULTY',
  'BALL_COUNT',
  'BALL_SPEED',
  'PADDLE_SIZE',
  'PADDLE_SPEED'
];

export class GameAI {
  constructor() {
    this.ai = new AIUtils();
    this.game = null;
    this.initialized = false;
    // Initialize upgrade levels for all upgrade types
    this.upgradeLevels = UPGRADES.reduce((acc, upgrade) => {
      acc[upgrade] = 0;
      return acc;
    }, {});
  }

  init() {
    if (!window.game || !window.game.ready) {
      setTimeout(() => this.init(), 100);
      return;
    }
    this.game = window.game;

    if (this.initialized) return;
    this.initialized = true;

    window.game.app.ticker.speed = this.ai.defaultGameSpeed;
    this.ai.updateDebugOverlay('Game speed set to ' + this.ai.defaultGameSpeed + 'x');

    if (this.ai.enabled) {
      this.ai.gameStartTime = Date.now();

      if (this.ai.mode === 'experimental') {
        this.setupExperimentalMode();
      }

      this.ai.startLoggingLoop(this.getMainCurrency.bind(this));
      this.startUpgradeLoop();
      this.updateGameStats();

      setTimeout(() => {
        this.ai.stopAI();
        this.ai.exportLogs();
        this.ai.updateDebugOverlay('Session ended - logs exported');
      }, this.ai.duration);
    }
  }

  getMainCurrency() {
    return this.game.money;
  }

  setupExperimentalMode() {
    // Give infinite money
    this.game.money = Number.MAX_SAFE_INTEGER;

    // Randomly upgrade each stat between 0-10 times
    UPGRADES.forEach(upgrade => {
      const times = Math.floor(Math.random() * 11); // 0 to 10
      for (let i = 0; i < times; i++) {
        this.performUpgrade(upgrade, 0, true);
      }
    });

    this.ai.updateDebugOverlay('Experimental mode initialized with random upgrades');
  }

  updateGameStats() {
    const stats = {
      Money: this.game.money,
      Score: this.game.score,
      'Ball Speed Level': this.upgradeLevels.BALL_SPEED,
      'Ball Count Level': this.upgradeLevels.BALL_COUNT,
      'Paddle Speed Level': this.upgradeLevels.PADDLE_SPEED,
      'Paddle Size Level': this.upgradeLevels.PADDLE_SIZE,
      'Difficulty Level': this.upgradeLevels.DIFFICULTY
    };

    this.ai.updateDebugOverlay('Game stats updated', stats);
  }

  startUpgradeLoop() {
    if (!this.ai.enabled || this.ai.mode === 'experimental') return;

    this.upgradeInterval = setInterval(() => {
      this.checkCheapestUpgrade();
      this.updateGameStats();
    }, 100);
  }

  checkCheapestUpgrade() {
    let cheapestUpgrade = null;
    let lowestCost = Infinity;

    for (const upgrade of UPGRADES) {
      const cost = this.game.upgradeCosts[upgrade];
      if (cost <= this.game.money && cost < lowestCost) {
        cheapestUpgrade = upgrade;
        lowestCost = cost;
      }
    }

    if (cheapestUpgrade) {
      this.performUpgrade(cheapestUpgrade, lowestCost);
    }
  }

  performUpgrade(upgradeName, cost, skipLogging = false) {
    // Increment the upgrade level before performing the upgrade
    this.upgradeLevels[upgradeName]++;
    const currentLevel = this.upgradeLevels[upgradeName];

    switch (upgradeName) {
      case 'BALL_SPEED':
        this.game.upgradeBallSpeed();
        break;
      case 'PADDLE_SPEED':
        this.game.upgradePaddleSpeed();
        break;
      case 'PADDLE_SIZE':
        this.game.upgradePaddleSize();
        break;
      case 'BALL_COUNT':
        this.game.addBall();
        break;
      case 'DIFFICULTY':
        this.game.upgradeDifficulty();
        break;
    }

    if (!skipLogging) {
      const upgradeInfo = {
        timestamp: Date.now(),
        upgrade: upgradeName,
        cost: cost,
        level: currentLevel
      };

      this.ai.logUpgrade(upgradeInfo);
      this.ai.updateDebugOverlay(`Purchased ${upgradeName} upgrade for ${cost} (Level ${currentLevel})`);
    }
  }
}

const gameAI = new GameAI();
gameAI.init();

if (window.game) {
  window.game.exportAILogs = () => gameAI.ai.exportLogs();
  window.game.clearAILogs = () => gameAI.ai.clearLogs();
}

export default gameAI;
```
__________________
Role: user
Content: The existing boilerplate codebase of the project is as follows:
```js src/Game.js
import React, { useRef, useState, useEffect } from 'react';
import { Settings } from 'lucide-react';
import { GameLogic } from './game/gameLogic';
import GameUI from './ui/GameUI';
import DebugUI from './ui/DebugUI';

const FRAME_RATE = 30;
const FRAME_INTERVAL = 1000 / FRAME_RATE;

const Game = () => {
  const containerRef = useRef(null);
  const gameRef = useRef(null);
  const [showDebugUI, setShowDebugUI] = useState(false);
  const [, setFrame] = useState(0);

  useEffect(() => {
    if (!containerRef.current) return;

    const game = new GameLogic(containerRef.current);
    window.game = game;
    gameRef.current = game;

    let lastTime = Date.now();
    let intervalId;
    const update = (currentTime) => {
      const deltaTime = (currentTime - lastTime) / 1000;
      lastTime = currentTime;

      // Force a re-render by updating the frame state
      setFrame(prevFrame => prevFrame + 1);
    };

    intervalId = setInterval(() => {
      update(Date.now());
    }, FRAME_INTERVAL);

    return () => {
      clearInterval(intervalId);
      if (gameRef.current) {
        gameRef.current.destroy();
        gameRef.current = null;
      }
      gameRef.current = null;
    };
  }, []);

  return (
    <div style={{
      position: 'relative',
      width: '800px',
      height: '600px',
      overflow: 'hidden'
    }}>
      <div ref={containerRef} style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%'
      }} />
      {gameRef.current && (
        <>
          <GameUI gameRef={gameRef} />
          {showDebugUI && <DebugUI gameRef={gameRef} />}
        </>
      )}
      <Settings
        onClick={() => setShowDebugUI(!showDebugUI)}
        style={{
          position: 'absolute',
          bottom: '10px',
          right: '10px',
          width: '24px',
          height: '24px',
          cursor: 'pointer',
          color: 'white'
        }}
      />
    </div>
  );
};

export default Game;
```
```js src/game/gameLogic.js
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

```
```js src/game/gameData.js
export const INITIAL_VALUES = {
  MONEY: 0,
  BARISTA_COUNT: 1,
  BARISTA_SPEED: 1,
  CUSTOMER_CAPACITY: 3,
  COFFEE_PRICE: 5,
  PROCESSING_SPEED: 1,
  CUSTOMER_SPAWN_RATE: 3, // seconds between spawns
  COFFEE_MAKE_TIME: 5, // seconds to make coffee
};

export const UPGRADE_COSTS = {
  BARISTA: 100,
  BARISTA_SPEED: 150,
  CUSTOMER_CAPACITY: 200,
  COFFEE_PRICE: 250,
  PROCESSING_SPEED: 300,
};

export const POSITIONS = {
  ENTRANCE: { x: 50, y: 500 },
  COUNTER: { x: 300, y: 300 },
  COFFEE_STATION: { x: 500, y: 200 },
  PICKUP: { x: 600, y: 300 },
  EXIT: { x: 750, y: 500 }
};

```
```js src/game/assetManifest.js
export const SPRITES = {
  background: {
    path: '/assets/background.png',
    width: 800,
    height: 600
  },
  barista: {
    path: '/assets/barista.png',
    width: 64,
    height: 64
  },
  customer: {
    path: '/assets/customer.png',
    width: 64,
    height: 64
  },
  counter: {
    path: '/assets/counter.png',
    width: 128,
    height: 64
  },
  coffee_station: {
    path: '/assets/coffee_station.png',
    width: 128,
    height: 64
  },
  pickup: {
    path: '/assets/pickup.png',
    width: 128,
    height: 64
  }
};

```
```js src/ui/GameUI.js
import React, { useState, useEffect } from 'react';

const Button = ({ onClick, children, cost }) => (
  <button onClick={onClick} style={{
    margin: '5px',
    padding: '5px 10px',
    fontSize: '14px',
    color: '#FFFFFF',
    border: 'none',
    cursor: 'pointer',
    backgroundColor: '#4A90E2',
  }}>
    {children} (${cost})
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#FFFFFF' }}>
    <p>Money: ${game.money} | Baristas: {game.baristaCount} | Customers: {game.customers?.children?.length || 0}/{game.customerCapacity} | Coffee Price: ${game.coffeePrice}</p>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current || !gameRef.current.ready) return null;

  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%', color: '#FFFFFF' }}>
      <HUD game={game} />
      <div style={{ position: 'absolute', bottom: '10px', left: '10px', right: '10px', textAlign: 'center' }}>
        <Button onClick={() => game.upgradeBarista()} cost={game.baristaCost}>
          Hire Barista
        </Button>
        <Button onClick={() => game.upgradeBaristaSpeed()} cost={game.baristaSpeedCost}>
          Upgrade Barista Speed
        </Button>
        <Button onClick={() => game.upgradeCustomerCapacity()} cost={game.customerCapacityCost}>
          Increase Customer Capacity
        </Button>
        <Button onClick={() => game.upgradeCoffeePrice()} cost={game.coffeePriceCost}>
          Increase Coffee Price
        </Button>
        <Button onClick={() => game.upgradeProcessingSpeed()} cost={game.processingSpeedCost}>
          Upgrade Processing Speed
        </Button>
      </div>
    </div>
  );
};

export default GameUI;

```

You should use this utility
```js src/AIUtils.js
export class AIUtils {
  constructor(config) {
    // Parse query parameters
    const params = new URLSearchParams(window.location.search);
    this.enabled = params.get('ai') === 'true';
    this.duration = parseInt(params.get('duration')) || 300000;
    this.logId = params.get('logId') || new Date().toISOString();
    this.defaultGameSpeed = parseFloat(params.get('speed')) || 1;
    this.mode = params.get('mode') || 'playthrough';

    this.initialized = false;
    this.gameStartTime = null;

    this.gameLog = [];
    this.lastLogTime = Date.now();
    this.logInterval = 1000;
    this.upgradeHistory = [];

    if (!localStorage.getItem('gameAILogs')) {
      localStorage.setItem('gameAILogs', JSON.stringify({}));
    }

    this.createDebugOverlay();
    this.createSettingsModal();
    this.updateDebugOverlay('Initializing AI...');
    this.startProgressUpdate();
  }

  createSettingsModal() {
    const modal = document.createElement('div');
    modal.id = 'ai-settings-modal';
    modal.style.cssText = `
      display: none;
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(0, 0, 0, 0.9);
      border: 1px solid #00ff00;
      padding: 20px;
      z-index: 10000;
      width: 300px;
      border-radius: 5px;
    `;

    const controls = document.createElement('div');
    controls.innerHTML = `
      <h3 style="color: #00ff00; margin-top: 0;">AI Settings</h3>
      <div style="margin-bottom: 10px;">
        <label style="display: flex; align-items: center;">
          <input type="checkbox" id="ai-enabled-modal" ${this.enabled ? 'checked' : ''}>
          <span style="margin-left: 5px; color: #00ff00;">Enable AI</span>
        </label>
      </div>
      <div style="margin-bottom: 10px;">
        <label style="color: #00ff00;">Mode:</label>
        <select id="ai-mode-modal" style="width: 100%; background: #004400; color: #00ff00; border: 1px solid #00ff00; margin-top: 5px;">
          <option value="playthrough" ${this.mode === 'playthrough' ? 'selected' : ''}>Playthrough</option>
          <option value="experimental" ${this.mode === 'experimental' ? 'selected' : ''}>Experimental</option>
        </select>
      </div>
      <div style="margin-bottom: 10px;">
        <label style="color: #00ff00;">Game Speed:</label>
        <input type="number" id="ai-speed-modal" value="${this.defaultGameSpeed}" step="0.1" min="0.1" max="10" 
          style="width: 100%; background: #004400; color: #00ff00; border: 1px solid #00ff00; margin-top: 5px;">
      </div>
      <div style="margin-bottom: 10px;">
        <label style="color: #00ff00;">Duration (s):</label>
        <input type="number" id="ai-duration-modal" value="${this.duration / 1000}" step="1" min="1" 
          style="width: 100%; background: #004400; color: #00ff00; border: 1px solid #00ff00; margin-top: 5px;">
      </div>
      <div style="margin-bottom: 15px;">
        <label style="color: #00ff00;">Log ID:</label>
        <input type="text" id="ai-logid-modal" value="${this.logId}" 
          style="width: 100%; background: #004400; color: #00ff00; border: 1px solid #00ff00; margin-top: 5px;">
      </div>
      <div style="display: flex; justify-content: space-between;">
        <button id="ai-settings-save" style="padding: 5px 15px; background: #004400; color: #00ff00; border: 1px solid #00ff00; cursor: pointer;">
          Save & Reload
        </button>
        <button id="ai-settings-close" style="padding: 5px 15px; background: #004400; color: #00ff00; border: 1px solid #00ff00; cursor: pointer;">
          Close
        </button>
      </div>
    `;

    modal.appendChild(controls);
    document.body.appendChild(modal);

    document.getElementById('ai-settings-save').addEventListener('click', () => {
      this.enabled = document.getElementById('ai-enabled-modal').checked;
      this.defaultGameSpeed = parseFloat(document.getElementById('ai-speed-modal').value);
      this.duration = parseInt(document.getElementById('ai-duration-modal').value) * 1000;
      this.logId = document.getElementById('ai-logid-modal').value;
      this.mode = document.getElementById('ai-mode-modal').value;

      const params = new URLSearchParams(window.location.search);
      params.set('debug', true);
      params.set('ai', this.enabled.toString());
      params.set('speed', this.defaultGameSpeed.toString());
      params.set('duration', this.duration.toString());
      params.set('logId', this.logId);
      params.set('mode', this.mode);
      window.history.replaceState({}, '', `${window.location.pathname}?${params}`);
      window.location.reload();
    });

    document.getElementById('ai-settings-close').addEventListener('click', () => {
      modal.style.display = 'none';
    });
  }

  createDebugOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'ai-debug-overlay';
    overlay.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      font-family: monospace;
      font-size: 12px;
      z-index: 9999;
      min-width: 20px;
      transition: all 0.3s ease;
      background: none;
    `;

    const header = document.createElement('div');
    header.style.cssText = `
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      user-select: none;
      white-space: nowrap;
    `;

    const iconElement = document.createElement('div');
    iconElement.innerHTML = '🤖';
    iconElement.style.cssText = `
      font-size: 20px;
      line-height: 1;
      opacity: 1;
      visibility: visible;
    `;

    const titleElement = document.createElement('span');
    titleElement.textContent = 'AI Control Panel';
    titleElement.style.cssText = `
      display: none;
      margin-left: 5px;
      color: #00ff00;
    `;

    const buttonsContainer = document.createElement('div');
    buttonsContainer.style.cssText = `
      display: none;
    `;
    buttonsContainer.innerHTML = `
      <button id="ai-settings-button" style="background: none; border: none; color: #00ff00; cursor: pointer; margin-right: 5px;">⚙️</button>
      <button id="ai-toggle-view" style="background: none; border: none; color: #00ff00; cursor: pointer;">▶</button>
    `;

    header.appendChild(iconElement);
    header.appendChild(titleElement);
    header.appendChild(buttonsContainer);

    const content = document.createElement('div');
    content.id = 'ai-content';
    content.style.cssText = `
      display: none;
      width: 280px;
      background: rgba(0, 0, 0, 0.8);
      padding: 10px;
      border-radius: 5px;
      margin-top: 5px;
      color: #00ff00;
    `;

    const statusDiv = document.createElement('div');
    statusDiv.innerHTML = `
      <div style="border-bottom: 1px solid #00ff00; margin-bottom: 5px; padding-bottom: 5px;">
        <div>AI Status: ${this.enabled ? 'Enabled' : 'Disabled'}</div>
        <div>Mode: ${this.mode}</div>
        <div>Speed: ${this.defaultGameSpeed}x</div>
        <div>Log ID: ${this.logId}</div>
        <div>Duration: ${this.duration / 1000}s</div>
        <div style="margin-top: 5px;">Progress:</div>
        <div style="background: #004400; height: 20px; border: 1px solid #00ff00; margin-top: 5px;">
          <div id="ai-progress-bar" style="background: #00ff00; height: 100%; width: 0%; transition: width 0.5s;"></div>
        </div>
        <div id="ai-time-remaining" style="text-align: center; margin-top: 2px;"></div>
      </div>
      <div id="ai-current-stats"></div>
      <div style="margin-top: 10px;" id="ai-last-action"></div>
      <div style="margin-top: 10px; border-top: 1px solid #00ff00; padding-top: 5px;">
        <div style="color: #00ff00; margin-bottom: 5px;">Upgrade History:</div>
        <div id="ai-upgrade-log" style="max-height: 150px; overflow-y: auto;"></div>
        <button id="ai-download-logs" style="margin-top: 10px; width: 100%; padding: 5px; background: #004400; color: #00ff00; border: 1px solid #00ff00; cursor: pointer;">Download Logs</button>
      </div>
    `;

    content.appendChild(statusDiv);
    overlay.appendChild(header);
    overlay.appendChild(content);
    document.body.appendChild(overlay);

    // Event listener modification
    header.addEventListener('click', () => {
      const content = document.getElementById('ai-content');
      const toggle = document.getElementById('ai-toggle-view');
      const titleElement = header.querySelector('span');
      const buttonsContainer = header.querySelector('div:last-child');
      const overlay = document.getElementById('ai-debug-overlay');

      if (content.style.display === 'none') {
        content.style.display = 'block';
        overlay.style.background = 'rgba(0, 0, 0, 0.8)';
        overlay.style.width = '300px';
        overlay.style.padding = '10px';
        overlay.style.borderRadius = '5px';
        titleElement.style.display = 'inline';
        buttonsContainer.style.display = 'inline';
        if (toggle) toggle.textContent = '▼';
      } else {
        content.style.display = 'none';
        overlay.style.background = 'none';
        overlay.style.width = 'auto';
        overlay.style.padding = '0';
        overlay.style.borderRadius = '0';
        titleElement.style.display = 'none';
        buttonsContainer.style.display = 'none';
        if (toggle) toggle.textContent = '▶';
      }
    });

    // Add event listeners for settings and download buttons
    document.getElementById('ai-settings-button')?.addEventListener('click', (e) => {
      e.stopPropagation(); // Prevent header click event
      document.getElementById('ai-settings-modal').style.display = 'block';
    });

    const downloadButton = document.getElementById('ai-download-logs');
    if (downloadButton) {
      downloadButton.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent header click event
        this.exportLogs();
      });
    }
  }

  startProgressUpdate() {
    if (!this.enabled) return;

    setInterval(() => {
      const elapsed = Date.now() - this.gameStartTime;
      const progress = Math.min((elapsed / this.duration) * 100, 100);
      const timeRemaining = Math.max(0, this.duration - elapsed);

      const progressBar = document.getElementById('ai-progress-bar');
      const timeRemainingDiv = document.getElementById('ai-time-remaining');

      if (progressBar && timeRemainingDiv) {
        progressBar.style.width = `${progress}%`;
        timeRemainingDiv.textContent = progress >= 100 ? 'AI Finished' : `${(timeRemaining / 1000).toFixed(1)}s remaining`;
      }
    }, 100);
  }

  updateDebugOverlay(action, stats = {}) {
    const statsDiv = document.getElementById('ai-current-stats');
    const lastAction = document.getElementById('ai-last-action');
    const upgradeLog = document.getElementById('ai-upgrade-log');

    if (statsDiv && lastAction) {
      const formatNumber = (num) => (num !== undefined && num !== null) ? Number(num).toFixed(0) : '0';

      statsDiv.innerHTML = Object.entries(stats)
        .map(([key, value]) => `<div>${key}: ${formatNumber(value)}</div>`)
        .join('');

      const timestamp = new Date().toLocaleTimeString();
      lastAction.innerHTML = `
        <div style="color: #888;">Last Action (${timestamp}):</div>
        <div style="color: #00ff00;">${action}</div>
      `;

      if (upgradeLog) {
        upgradeLog.innerHTML = this.upgradeHistory
          .map(upgrade => `
            <div style="margin-bottom: 3px; font-size: 11px; color: #888;">
              ${new Date(upgrade.timestamp).toLocaleTimeString()} - ${upgrade.upgrade} (Level ${upgrade.level}) - Cost: ${upgrade.cost}
            </div>
          `)
          .join('');

        upgradeLog.scrollTop = upgradeLog.scrollHeight;
      }
    }
  }

  stopAI() {
    this.enabled = false;
    this.updateDebugOverlay('AI Finished');
    clearInterval(this.loggingInterval);
    clearInterval(this.upgradeInterval);
  }

  startLoggingLoop(getCurrencyFn) {
    if (!this.enabled) return;

    this.loggingInterval = setInterval(() => {
      const logEntry = {
        timestamp: Date.now(),
        timeElapsed: Date.now() - this.gameStartTime,
        currency: getCurrencyFn()
      };

      this.gameLog.push(logEntry);
      this.saveLogsToStorage();
      this.updateDebugOverlay('Logged game state');
    }, this.logInterval);
  }

  logUpgrade(upgradeInfo) {
    const timestamp = Date.now();

    // For display in overlay
    this.upgradeHistory.push({
      ...upgradeInfo,
      timestamp: timestamp
    });

    if (this.upgradeHistory.length > 50) {
      this.upgradeHistory.shift();
    }

    // For logging to file
    const upgradeLog = {
      timestamp: timestamp,
      timeElapsed: timestamp - this.gameStartTime,
      type: 'upgrade',
      ...upgradeInfo
    };

    this.gameLog.push(upgradeLog);
    this.saveLogsToStorage();
  }

  saveLogsToStorage() {
    if (!this.enabled) return;

    try {
      const allLogs = JSON.parse(localStorage.getItem('gameAILogs') || '{}');
      allLogs[this.logId] = this.gameLog;
      localStorage.setItem('gameAILogs', JSON.stringify(allLogs));
    } catch (error) {
      console.error('Failed to save game logs:', error);
      this.updateDebugOverlay('Error: Failed to save logs');
    }
  }

  exportLogs() {
    try {
      if (this.gameLog.length === 0) {
        this.updateDebugOverlay('Warning: No logs to export');
        return;
      }

      const blob = new Blob([JSON.stringify(this.gameLog, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = url;
      a.download = `game-ai-logs-${this.logId}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      this.updateDebugOverlay(`Logs exported successfully (${this.gameLog.length} entries)`);
    } catch (error) {
      console.error('Failed to export logs:', error);
      this.updateDebugOverlay('Error: Failed to export logs');
    }
  }

  clearLogs() {
    if (!this.enabled) return;

    localStorage.setItem('gameAILogs', JSON.stringify({}));
    this.gameLog = [];
    this.updateDebugOverlay('Logs cleared');
  }
}

```

Fill out the functionality of this boilerplate
```js src/GameAI.js
import { AIUtils } from './AIUtils';
import { /* bring in all the relevant immutable data from game data */ } from './game/gameData';

const UPGRADES = [
  // enumerate all the possible upgrades in this game
];

export class GameAI {
  constructor() {
    this.ai = new AIUtils();
    this.game = null;
    this.initialized = false;
    // Initialize upgrade levels for all upgrade types
    this.upgradeLevels = UPGRADES.reduce((acc, upgrade) => {
      acc[upgrade] = 0;
      return acc;
    }, {});
  }

  init() {
    if (!window.game || !window.game.ready) {
      setTimeout(() => this.init(), 100);
      return;
    }
    this.game = window.game;

    if (this.initialized) return;
    this.initialized = true;

    window.game.app.ticker.speed = this.ai.defaultGameSpeed;
    this.ai.updateDebugOverlay('Game speed set to ' + this.ai.defaultGameSpeed + 'x');

    if (this.ai.enabled) {
      this.ai.gameStartTime = Date.now();

      if (this.ai.mode === 'experimental') {
        this.setupExperimentalMode();
      }

      this.ai.startLoggingLoop(this.getMainCurrency.bind(this));
      this.startUpgradeLoop();
      this.updateGameStats();

      setTimeout(() => {
        this.ai.stopAI();
        this.ai.exportLogs();
        this.ai.updateDebugOverlay('Session ended - logs exported');
      }, this.ai.duration);
    }
  }

  getMainCurrency() {
    // get the up-to-date count of the main currency
  }

  setupExperimentalMode() {
    // Give infinite currency for experimental mode
    // this.game.mainCurrencyValue = Number.MAX_SAFE_INTEGER;

    // Randomly upgrade each stat between 0-10 times
    UPGRADES.forEach(upgrade => {
      const times = Math.floor(Math.random() * 11); // 0 to 10
      for (let i = 0; i < times; i++) {
        this.performUpgrade(upgrade, 0, true);
      }
    });

    this.ai.updateDebugOverlay('Experimental mode initialized with random upgrades');
  }

  updateGameStats() {
    const stats = {
      // show all the relevant game stats here
    };

    this.ai.updateDebugOverlay('Game stats updated', stats);
  }

  startUpgradeLoop() {
    if (!this.ai.enabled || this.ai.mode === 'experimental') return;

    this.upgradeInterval = setInterval(() => {
      this.checkCheapestUpgrade();
      this.updateGameStats();
    }, 100);
  }

  checkCheapestUpgrade() {
    // find the cheapest upgrade and buy it
  }

  performUpgrade(upgradeName, cost, skipLogging = false) {
    // Increment the upgrade level before performing the upgrade
    this.upgradeLevels[upgradeName]++;
    const currentLevel = this.upgradeLevels[upgradeName];

    switch (upgradeName) {
      // handle each possible upgrade here
      default:
        console.error(`${upgradeName} is not a valid upgrade`)
    }

    if (!skipLogging) {
      const upgradeInfo = {
        timestamp: Date.now(),
        upgrade: upgradeName,
        cost: cost,
        level: currentLevel
      };

      this.ai.logUpgrade(upgradeInfo);
      this.ai.updateDebugOverlay(`Purchased ${upgradeName} upgrade for ${cost} (Level ${currentLevel})`);
    }
  }
}

const gameAI = new GameAI();
gameAI.init();

if (window.game) {
  window.game.exportAILogs = () => gameAI.ai.exportLogs();
  window.game.clearAILogs = () => gameAI.ai.clearLogs();
}

export default gameAI;
```

Only make changes to the GameAI file. Don't change anything about the game logic just fill out the GameAI code and use the AIUtils

Some explanation about the different AI modes: experimental mode sets the upgrades randomly so we can observe how a certain set of upgrades affect the game. The standard mode buys the cheapest upgrade at any time

General Implementation Guidelines:
1. Write out all the code of the files you intend to edit. I will be copy-pasting them
2. Do not create new files, add to the existing files in the appropriate locations
3. Do not do any refactoring outside of what you are requested to do

Directions:
In your response, do both steps, one after the other
1. First think carefully and describe in detail how you will implement the game design. Make sure to follow all the guidelines
2. Then write each file, according to the plan

Write out all the files in the format:
```filetype filepath
content
```

MOST IMPORTANT: Do not write "existing code here" or similar placeholders. If a file has been edited in anyway,
EVERY original unchanged line must be rewritten in your output
__________________
Role: assistant
Content: Let me plan out the implementation first:

1. Implementation Plan:
- The game is a coffee shop management game where we need to manage baristas, customer capacity, and various upgrades
- We need to track all possible upgrades in the UPGRADES constant:
  * BARISTA (hire new barista)
  * BARISTA_SPEED (make baristas work faster)
  * CUSTOMER_CAPACITY (allow more customers)
  * COFFEE_PRICE (increase price per coffee)
  * PROCESSING_SPEED (make coffee preparation faster)

- For getMainCurrency():
  * Return game.money which is the main currency

- For updateGameStats():
  * Track money, barista count, customer count, coffee price
  * Track all upgrade levels and costs

- For checkCheapestUpgrade():
  * Compare costs of all available upgrades
  * Buy the cheapest one we can afford

- For performUpgrade():
  * Handle each upgrade type by calling corresponding game method
  * Track upgrade levels
  * Log the upgrade for AI analysis

2. Implementation:

```javascript src/GameAI.js
import { AIUtils } from './AIUtils';
import { INITIAL_VALUES, UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'BARISTA',
  'BARISTA_SPEED',
  'CUSTOMER_CAPACITY', 
  'COFFEE_PRICE',
  'PROCESSING_SPEED'
];

export class GameAI {
  constructor() {
    this.ai = new AIUtils();
    this.game = null;
    this.initialized = false;
    // Initialize upgrade levels for all upgrade types
    this.upgradeLevels = UPGRADES.reduce((acc, upgrade) => {
      acc[upgrade] = 0;
      return acc;
    }, {});
  }

  init() {
    if (!window.game || !window.game.ready) {
      setTimeout(() => this.init(), 100);
      return;
    }
    this.game = window.game;

    if (this.initialized) return;
    this.initialized = true;

    window.game.app.ticker.speed = this.ai.defaultGameSpeed;
    this.ai.updateDebugOverlay('Game speed set to ' + this.ai.defaultGameSpeed + 'x');

    if (this.ai.enabled) {
      this.ai.gameStartTime = Date.now();

      if (this.ai.mode === 'experimental') {
        this.setupExperimentalMode();
      }

      this.ai.startLoggingLoop(this.getMainCurrency.bind(this));
      this.startUpgradeLoop();
      this.updateGameStats();

      setTimeout(() => {
        this.ai.stopAI();
        this.ai.exportLogs();
        this.ai.updateDebugOverlay('Session ended - logs exported');
      }, this.ai.duration);
    }
  }

  getMainCurrency() {
    return this.game.money;
  }

  setupExperimentalMode() {
    // Give infinite money for experimental mode
    this.game.money = Number.MAX_SAFE_INTEGER;

    // Randomly upgrade each stat between 0-10 times
    UPGRADES.forEach(upgrade => {
      const times = Math.floor(Math.random() * 11); // 0 to 10
      for (let i = 0; i < times; i++) {
        this.performUpgrade(upgrade, 0, true);
      }
    });

    this.ai.updateDebugOverlay('Experimental mode initialized with random upgrades');
  }

  updateGameStats() {
    const stats = {
      Money: this.game.money,
      'Barista Count': this.game.baristaCount,
      'Customer Count': this.game.customers?.children?.length || 0,
      'Customer Capacity': this.game.customerCapacity,
      'Coffee Price': this.game.coffeePrice,
      'Processing Speed': this.game.processingSpeed.toFixed(2),
      'Barista Speed': this.game.baristaSpeed.toFixed(2),
      'Barista Cost': this.game.baristaCost,
      'Speed Cost': this.game.baristaSpeedCost,
      'Capacity Cost': this.game.customerCapacityCost,
      'Price Cost': this.game.coffeePriceCost,
      'Processing Cost': this.game.processingSpeedCost
    };

    this.ai.updateDebugOverlay('Game stats updated', stats);
  }

  startUpgradeLoop() {
    if (!this.ai.enabled || this.ai.mode === 'experimental') return;

    this.upgradeInterval = setInterval(() => {
      this.checkCheapestUpgrade();
      this.updateGameStats();
    }, 100);
  }

  checkCheapestUpgrade() {
    let cheapestUpgrade = null;
    let lowestCost = Infinity;

    const upgradeCosts = {
      BARISTA: this.game.baristaCost,
      BARISTA_SPEED: this.game.baristaSpeedCost,
      CUSTOMER_CAPACITY: this.game.customerCapacityCost,
      COFFEE_PRICE: this.game.coffeePriceCost,
      PROCESSING_SPEED: this.game.processingSpeedCost
    };

    for (const upgrade of UPGRADES) {
      const cost = upgradeCosts[upgrade];
      if (cost <= this.game.money && cost < lowestCost) {
        cheapestUpgrade = upgrade;
        lowestCost = cost;
      }
    }

    if (cheapestUpgrade) {
      this.performUpgrade(cheapestUpgrade, lowestCost);
    }
  }

  performUpgrade(upgradeName, cost, skipLogging = false) {
    // Increment the upgrade level before performing the upgrade
    this.upgradeLevels[upgradeName]++;
    const currentLevel = this.upgradeLevels[upgradeName];

    switch (upgradeName) {
      case 'BARISTA':
        this.game.upgradeBarista();
        break;
      case 'BARISTA_SPEED':
        this.game.upgradeBaristaSpeed();
        break;
      case 'CUSTOMER_CAPACITY':
        this.game.upgradeCustomerCapacity();
        break;
      case 'COFFEE_PRICE':
        this.game.upgradeCoffeePrice();
        break;
      case 'PROCESSING_SPEED':
        this.game.upgradeProcessingSpeed();
        break;
      default:
        console.error(`${upgradeName} is not a valid upgrade`);
    }

    if (!skipLogging) {
      const upgradeInfo = {
        timestamp: Date.now(),
        upgrade: upgradeName,
        cost: cost,
        level: currentLevel
      };

      this.ai.logUpgrade(upgradeInfo);
      this.ai.updateDebugOverlay(`Purchased ${upgradeName} upgrade for ${cost} (Level ${currentLevel})`);
    }
  }
}

const gameAI = new GameAI();
gameAI.init();

if (window.game) {
  window.game.exportAILogs = () => gameAI.ai.exportLogs();
  window.game.clearAILogs = () => gameAI.ai.clearLogs();
}

export default gameAI;
```

This implementation:
1. Defines all possible upgrades
2. Tracks upgrade levels
3. Implements experimental mode with random upgrades
4. Implements standard mode that buys cheapest available upgrade
5. Tracks and logs all game stats and upgrades
6. Uses the AIUtils for logging and UI updates
7. Maintains compatibility with the existing game logic

The AI will automatically buy upgrades in order of cost, allowing for efficient progression through the game.
__________________
