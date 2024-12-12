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
import { INITIAL_VALUES, UPGRADE_COSTS, GAMEPLAY } from './gameData';
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

    this.ready = false;
    this.credits = 0;
    this.tankSpeed = INITIAL_VALUES.TANK_SPEED;
    this.tankHealth = INITIAL_VALUES.TANK_HEALTH;
    this.tankDamage = INITIAL_VALUES.TANK_DAMAGE;
    this.tankFireRate = INITIAL_VALUES.TANK_FIRE_RATE;
    this.tankRange = INITIAL_VALUES.TANK_RANGE;
    this.tankCount = INITIAL_VALUES.TANK_COUNT;

    this.costs = {...UPGRADE_COSTS};
    
    this.enemySpawnTimer = 0;
    this.lastTimestamp = performance.now();

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop);
      this.ready = true;
    });
  }

  getSprite = (spriteConfig) => {
    const texture = PIXI.Texture.from(spriteConfig.path);
    const sprite = new PIXI.Sprite(texture);
    sprite.width = spriteConfig.width;
    sprite.height = spriteConfig.height;
    return sprite;
  }

  createGameObjects = () => {
    this.background = this.getSprite(SPRITES.background);
    this.tanks = new PIXI.Container();
    this.enemies = new PIXI.Container();
    this.bullets = new PIXI.Container();
    this.healthBars = new PIXI.Container();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.tanks);
    this.app.stage.addChild(this.enemies);
    this.app.stage.addChild(this.bullets);
    this.app.stage.addChild(this.healthBars);

    for (let i = 0; i < this.tankCount; i++) {
      this.createTank();
    }
  }

  createTank = () => {
    const tank = this.getSprite(SPRITES.friendlyTank);
    tank.anchor.set(0.5);
    tank.x = SCREEN_SIZE.width / 2;
    tank.y = SCREEN_SIZE.height / 2;
    tank.health = this.tankHealth;
    tank.fireTimer = 0;
    this.tanks.addChild(tank);
    this.createHealthBar(tank);
  }

  createEnemy = () => {
    const enemy = this.getSprite(SPRITES.enemyTank);
    enemy.anchor.set(0.5);
    
    const side = Math.floor(Math.random() * 4);
    switch(side) {
      case 0:
        enemy.x = Math.random() * SCREEN_SIZE.width;
        enemy.y = -32;
        break;
      case 1:
        enemy.x = SCREEN_SIZE.width + 32;
        enemy.y = Math.random() * SCREEN_SIZE.height;
        break;
      case 2:
        enemy.x = Math.random() * SCREEN_SIZE.width;
        enemy.y = SCREEN_SIZE.height + 32;
        break;
      case 3:
        enemy.x = -32;
        enemy.y = Math.random() * SCREEN_SIZE.height;
        break;
    }
    
    enemy.health = GAMEPLAY.ENEMY_HEALTH;
    this.enemies.addChild(enemy);
    this.createHealthBar(enemy);
  }

  createHealthBar = (entity) => {
    const bar = new PIXI.Graphics();
    bar.beginFill(0x00ff00);
    bar.drawRect(-25, -40, 50, 5);
    bar.endFill();
    bar.owner = entity;
    this.healthBars.addChild(bar);
  }

  createBullet = (shooter, target) => {
    const bullet = new PIXI.Graphics();
    bullet.beginFill(0xffff00);
    bullet.drawCircle(0, 0, 3);
    bullet.endFill();
    bullet.x = shooter.x;
    bullet.y = shooter.y;
    
    const angle = Math.atan2(target.y - shooter.y, target.x - shooter.x);
    bullet.rotation = angle;
    bullet.dx = Math.cos(angle) * GAMEPLAY.BULLET_SPEED;
    bullet.dy = Math.sin(angle) * GAMEPLAY.BULLET_SPEED;
    bullet.damage = shooter.parent === this.tanks ? this.tankDamage : GAMEPLAY.ENEMY_DAMAGE;
    
    this.bullets.addChild(bullet);
  }

  gameLoop = (delta) => {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.enemySpawnTimer += elapsedSecs;
    if (this.enemySpawnTimer >= INITIAL_VALUES.ENEMY_SPAWN_RATE) {
      this.createEnemy();
      this.enemySpawnTimer = 0;
    }

    this.updateTanks(elapsedSecs);
    this.updateEnemies(elapsedSecs);
    this.updateBullets(elapsedSecs);
    this.updateHealthBars();
  }

  updateTanks = (elapsedSecs) => {
    this.tanks.children.forEach(tank => {
      const target = this.findNearestEnemy(tank);
      if (target) {
        const dx = target.x - tank.x;
        const dy = target.y - tank.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        tank.rotation = Math.atan2(dy, dx);

        if (distance > this.tankRange) {
          tank.x += (dx / distance) * this.tankSpeed * elapsedSecs;
          tank.y += (dy / distance) * this.tankSpeed * elapsedSecs;
        }

        tank.fireTimer += elapsedSecs;
        if (tank.fireTimer >= 1 / this.tankFireRate) {
          this.createBullet(tank, target);
          tank.fireTimer = 0;
        }
      }
    });
  }

  updateEnemies = (elapsedSecs) => {
    this.enemies.children.forEach(enemy => {
      const dx = SCREEN_SIZE.width/2 - enemy.x;
      const dy = SCREEN_SIZE.height/2 - enemy.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      enemy.rotation = Math.atan2(dy, dx);

      enemy.x += (dx / distance) * GAMEPLAY.ENEMY_SPEED * elapsedSecs;
      enemy.y += (dy / distance) * GAMEPLAY.ENEMY_SPEED * elapsedSecs;
    });
  }

  updateBullets = (elapsedSecs) => {
    this.bullets.children.forEach(bullet => {
      bullet.x += bullet.dx * elapsedSecs;
      bullet.y += bullet.dy * elapsedSecs;

      if (bullet.x < 0 || bullet.x > SCREEN_SIZE.width || 
          bullet.y < 0 || bullet.y > SCREEN_SIZE.height) {
        this.bullets.removeChild(bullet);
        return;
      }

      const targets = bullet.damage === this.tankDamage ? this.enemies : this.tanks;
      targets.children.forEach(target => {
        if (this.checkCollision(bullet, target)) {
          target.health -= bullet.damage;
          this.bullets.removeChild(bullet);
          
          if (target.health <= 0) {
            if (targets === this.enemies) {
              this.credits += INITIAL_VALUES.CREDITS_PER_KILL;
            }
            this.removeEntity(target);
          }
        }
      });
    });
  }

  updateHealthBars = () => {
    this.healthBars.children.forEach(bar => {
      if (!bar.owner.parent) {
        this.healthBars.removeChild(bar);
        return;
      }
      bar.x = bar.owner.x;
      bar.y = bar.owner.y;
      bar.scale.x = bar.owner.health / (bar.owner.parent === this.tanks ? this.tankHealth : GAMEPLAY.ENEMY_HEALTH);
    });
  }

  findNearestEnemy = (tank) => {
    let nearest = null;
    let minDistance = Infinity;
    
    this.enemies.children.forEach(enemy => {
      const dx = enemy.x - tank.x;
      const dy = enemy.y - tank.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < minDistance) {
        minDistance = distance;
        nearest = enemy;
      }
    });
    
    return nearest;
  }

  checkCollision = (obj1, obj2) => {
    const dx = obj1.x - obj2.x;
    const dy = obj1.y - obj2.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    return distance < (obj1.width + obj2.width) / 4;
  }

  removeEntity = (entity) => {
    entity.parent.removeChild(entity);
  }

  upgradeTankSpeed = () => {
    if (this.credits >= this.costs.TANK_SPEED) {
      this.credits -= this.costs.TANK_SPEED;
      this.tankSpeed *= 1.1;
      this.costs.TANK_SPEED *= 2;
    }
  }

  upgradeTankHealth = () => {
    if (this.credits >= this.costs.TANK_HEALTH) {
      this.credits -= this.costs.TANK_HEALTH;
      this.tankHealth *= 1.2;
      this.costs.TANK_HEALTH *= 2;
    }
  }

  upgradeTankDamage = () => {
    if (this.credits >= this.costs.TANK_DAMAGE) {
      this.credits -= this.costs.TANK_DAMAGE;
      this.tankDamage *= 1.2;
      this.costs.TANK_DAMAGE *= 2;
    }
  }

  upgradeFireRate = () => {
    if (this.credits >= this.costs.TANK_FIRE_RATE) {
      this.credits -= this.costs.TANK_FIRE_RATE;
      this.tankFireRate *= 1.1;
      this.costs.TANK_FIRE_RATE *= 2;
    }
  }

  upgradeRange = () => {
    if (this.credits >= this.costs.TANK_RANGE) {
      this.credits -= this.costs.TANK_RANGE;
      this.tankRange *= 1.1;
      this.costs.TANK_RANGE *= 2;
    }
  }

  upgradeTankCount = () => {
    if (this.credits >= this.costs.TANK_COUNT) {
      this.credits -= this.costs.TANK_COUNT;
      this.tankCount++;
      this.createTank();
      this.costs.TANK_COUNT *= 2;
    }
  }

  destroy = () => {
    this.app.destroy(true);
  }
}

```
```js src/game/gameData.js
export const INITIAL_VALUES = {
  TANK_SPEED: 100, // pixels per second
  TANK_HEALTH: 100,
  TANK_DAMAGE: 20,
  TANK_FIRE_RATE: 1, // shots per second
  TANK_RANGE: 200, // pixels
  TANK_COUNT: 1,
  ENEMY_SPAWN_RATE: 2, // seconds between spawns
  CREDITS_PER_KILL: 10
};

export const UPGRADE_COSTS = {
  TANK_SPEED: 10,
  TANK_HEALTH: 15,
  TANK_DAMAGE: 20,
  TANK_FIRE_RATE: 25,
  TANK_RANGE: 30,
  TANK_COUNT: 50
};

export const GAMEPLAY = {
  ENEMY_SPEED: 60,
  ENEMY_HEALTH: 50,
  ENEMY_DAMAGE: 10,
  BULLET_SPEED: 300
};

```
```js src/game/assetManifest.js
export const SPRITES = {
  background: {
    path: 'assets/background.png',
    width: 800,
    height: 600
  },
  friendlyTank: {
    path: 'assets/friendly_tank.png',
    width: 64,
    height: 64
  },
  enemyTank: {
    path: 'assets/enemy_tank.png',
    width: 64,
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
    color: '#d3d3d3',
    border: 'none',
    cursor: 'pointer',
    backgroundColor: '#7C45CB',
    position: 'relative',
  }}>
    {children} ({cost} credits)
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#d3d3d3' }}>
    <p>Credits: {game.credits} | Tanks: {game.tankCount} | Speed: {game.tankSpeed.toFixed(1)} | Health: {game.tankHealth.toFixed(0)} | Damage: {game.tankDamage.toFixed(1)} | Fire Rate: {game.tankFireRate.toFixed(1)} | Range: {game.tankRange.toFixed(0)}</p>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%', color: '#d3d3d3' }}>
      <HUD game={game} />
      <div style={{ position: 'absolute', bottom: '10px', left: '10px', right: '10px', textAlign: 'center' }}>
        <Button onClick={() => game.upgradeTankCount()} cost={game.costs.TANK_COUNT}>Add Tank</Button>
        <Button onClick={() => game.upgradeTankSpeed()} cost={game.costs.TANK_SPEED}>Upgrade Speed</Button>
        <Button onClick={() => game.upgradeTankHealth()} cost={game.costs.TANK_HEALTH}>Upgrade Health</Button>
        <Button onClick={() => game.upgradeTankDamage()} cost={game.costs.TANK_DAMAGE}>Upgrade Damage</Button>
        <Button onClick={() => game.upgradeFireRate()} cost={game.costs.TANK_FIRE_RATE}>Upgrade Fire Rate</Button>
        <Button onClick={() => game.upgradeRange()} cost={game.costs.TANK_RANGE}>Upgrade Range</Button>
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
- The game is a tank defense game where you upgrade various tank attributes
- Main currency is "credits" earned from killing enemies
- Need to track upgrades for: TANK_SPEED, TANK_HEALTH, TANK_DAMAGE, TANK_FIRE_RATE, TANK_RANGE, TANK_COUNT
- For experimental mode:
  * Set credits to max value
  * Randomly apply 0-10 upgrades for each upgrade type
- For standard mode:
  * Check costs of all possible upgrades
  * Buy the cheapest one available
- Need to track stats like:
  * Current credits
  * Number of tanks
  * Tank speed, health, damage, fire rate, range
  * Current upgrade costs
- Will use the AIUtils for:
  * Logging upgrades and currency over time
  * Displaying debug overlay
  * Managing experimental vs standard modes
  * Controlling game speed

2. Here's the implementation:

```javascript src/GameAI.js
import { AIUtils } from './AIUtils';
import { INITIAL_VALUES, UPGRADE_COSTS } from './game/gameData';

const UPGRADES = [
  'TANK_SPEED',
  'TANK_HEALTH', 
  'TANK_DAMAGE',
  'TANK_FIRE_RATE',
  'TANK_RANGE',
  'TANK_COUNT'
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
    return this.game.credits;
  }

  setupExperimentalMode() {
    // Give infinite currency for experimental mode
    this.game.credits = Number.MAX_SAFE_INTEGER;

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
      Credits: this.game.credits,
      'Tank Count': this.game.tankCount,
      'Tank Speed': this.game.tankSpeed.toFixed(1),
      'Tank Health': this.game.tankHealth.toFixed(0),
      'Tank Damage': this.game.tankDamage.toFixed(1),
      'Fire Rate': this.game.tankFireRate.toFixed(1),
      'Tank Range': this.game.tankRange.toFixed(0),
      'Speed Cost': this.game.costs.TANK_SPEED,
      'Health Cost': this.game.costs.TANK_HEALTH,
      'Damage Cost': this.game.costs.TANK_DAMAGE,
      'Fire Rate Cost': this.game.costs.TANK_FIRE_RATE,
      'Range Cost': this.game.costs.TANK_RANGE,
      'Tank Count Cost': this.game.costs.TANK_COUNT
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
      const cost = this.game.costs[upgrade];
      if (cost <= this.game.credits && cost < lowestCost) {
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
      case 'TANK_SPEED':
        this.game.upgradeTankSpeed();
        break;
      case 'TANK_HEALTH':
        this.game.upgradeTankHealth();
        break;
      case 'TANK_DAMAGE':
        this.game.upgradeTankDamage();
        break;
      case 'TANK_FIRE_RATE':
        this.game.upgradeFireRate();
        break;
      case 'TANK_RANGE':
        this.game.upgradeRange();
        break;
      case 'TANK_COUNT':
        this.game.upgradeTankCount();
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
5. Tracks and displays all relevant game stats
6. Uses AIUtils for logging and debug display
7. Properly handles both game modes
8. Maintains upgrade history and logging

The AI will continuously buy the cheapest available upgrade in standard mode, while experimental mode will randomly apply upgrades to see how different combinations affect gameplay.
__________________
