import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS } from './gameData';
import { SPRITES } from './assetManifest';
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
    this.gold = 0;
    this.lastTimestamp = performance.now();
    
    // Game attributes
    this.minerCount = INITIAL_VALUES.MINER_COUNT;
    this.miningSpeed = INITIAL_VALUES.MINING_SPEED;
    this.carryingCapacity = INITIAL_VALUES.CARRYING_CAPACITY;
    this.maxMines = INITIAL_VALUES.MAX_MINES;
    this.mineSize = INITIAL_VALUES.MINE_SIZE;

    // Upgrade costs
    this.minerCost = UPGRADE_COSTS.MINER_COUNT;
    this.speedCost = UPGRADE_COSTS.MINING_SPEED;
    this.capacityCost = UPGRADE_COSTS.CARRYING_CAPACITY;
    this.maxMinesCost = UPGRADE_COSTS.MAX_MINES;
    this.mineSizeCost = UPGRADE_COSTS.MINE_SIZE;

    const loader = PIXI.Loader.shared;
    Object.values(SPRITES).forEach(sprite => {
      loader.add(sprite.path);
    });
    
    loader.load(() => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(spriteConfig) {
    const sprite = new PIXI.Sprite(PIXI.Texture.from(SPRITES[spriteConfig].path));
    sprite.width = SPRITES[spriteConfig].width;
    sprite.height = SPRITES[spriteConfig].height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite('background');
    
    // Create depot container
    this.depotContainer = new PIXI.Container();
    const depotSprite = this.getSprite('depot');
    depotSprite.anchor.set(0.5);
    this.depotContainer.addChild(depotSprite);
    this.depotContainer.x = SCREEN_SIZE.width / 2;
    this.depotContainer.y = SCREEN_SIZE.height / 2;

    // Create particle system for depot
    this.effects.createParticleSystem(this.depotContainer, {
      maxParticles: 20,
      radius: 30,
      spawnInterval: 5
    });

    // Containers for miners and mines
    this.miners = new PIXI.Container();
    this.mines = new PIXI.Container();

    // Create initial miners and mines
    for (let i = 0; i < this.minerCount; i++) {
      this.createMiner();
    }
    
    for (let i = 0; i < this.maxMines; i++) {
      this.createMine();
    }

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.depotContainer);
    this.app.stage.addChild(this.mines);
    this.app.stage.addChild(this.miners);
  }

  createMiner() {
    const minerContainer = new PIXI.Container();
    const minerSprite = this.getSprite('miner');
    minerSprite.anchor.set(0.5);
    
    // Add shadow
    this.effects.createShadow(minerContainer, minerSprite);
    
    minerContainer.addChild(minerSprite);
    minerContainer.x = this.depotContainer.x;
    minerContainer.y = this.depotContainer.y;
    minerContainer.carrying = 0;
    minerContainer.targetMine = null;
    minerContainer.state = 'seeking';
    minerContainer.sprite = minerSprite;

    // Add idle animation
    this.effects.idleAnimation(minerSprite);

    this.miners.addChild(minerContainer);
    
    // Spawn animation
    this.effects.spawnAnimation(minerContainer);
  }

  createMine() {
    const mineContainer = new PIXI.Container();
    const mineSprite = this.getSprite('mine');
    mineSprite.anchor.set(0.5);
    
    let validPosition = false;
    while (!validPosition) {
      const x = Math.random() * (SCREEN_SIZE.width - 100) + 50;
      const y = Math.random() * (SCREEN_SIZE.height - 100) + 50;
      
      const distToDepot = Math.hypot(x - this.depotContainer.x, y - this.depotContainer.y);
      if (distToDepot < 100) continue;
      
      validPosition = true;
      mineContainer.x = x;
      mineContainer.y = y;
    }
    
    mineContainer.addChild(mineSprite);
    mineContainer.goldAmount = this.mineSize;
    mineContainer.sprite = mineSprite;
    
    // Add shadow
    this.effects.createShadow(mineContainer, mineSprite);
    
    this.mines.addChild(mineContainer);
    
    // Spawn animation
    this.effects.spawnAnimation(mineContainer);
  }

  gameLoop() {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    this.updateMiners(elapsedSecs);
    this.manageMines();
  }

  updateMiners(elapsedSecs) {
    this.miners.children.forEach(miner => {
      if (miner.state === 'seeking') {
        if (!miner.targetMine || miner.targetMine.goldAmount <= 0) {
          miner.targetMine = this.findNearestMine(miner);
        }
        
        if (miner.targetMine) {
          const arrived = this.moveTo(miner, miner.targetMine, elapsedSecs);
          if (arrived) {
            const mined = Math.min(this.carryingCapacity, miner.targetMine.goldAmount);
            miner.carrying = mined;
            miner.targetMine.goldAmount -= mined;
            
            // Mining effects
            this.effects.createImpactEffect(miner.targetMine);
            this.effects.showFloatingText(miner.targetMine, `+${mined}`);
            this.effects.createSpiralParticles(miner.targetMine);
            
            miner.state = 'returning';
          }
        }
      } else if (miner.state === 'returning') {
        const arrived = this.moveTo(miner, this.depotContainer, elapsedSecs);
        if (arrived) {
          this.gold += miner.carrying;
          
          // Delivery effects
          this.effects.createSpiralParticles(this.depotContainer, {
            color: 0xFFD700
          });
          this.effects.showFloatingText(this.depotContainer, `+${miner.carrying}`);
          
          miner.carrying = 0;
          miner.state = 'seeking';
        }
      }
    });
  }

  moveTo(mover, target, elapsedSecs) {
    const dx = target.x - mover.x;
    const dy = target.y - mover.y;
    const distance = Math.hypot(dx, dy);
    
    if (distance < 5) return true;
    
    const moveDistance = this.miningSpeed * elapsedSecs;
    const ratio = Math.min(moveDistance / distance, 1);
    
    mover.x += dx * ratio;
    mover.y += dy * ratio;
    
    // Rotate miner to face movement direction
    mover.rotation = Math.atan2(dy, dx);
    
    return false;
  }

  findNearestMine(miner) {
    let nearest = null;
    let minDistance = Infinity;
    
    this.mines.children.forEach(mine => {
      if (mine.goldAmount <= 0) return;
      const distance = Math.hypot(mine.x - miner.x, mine.y - miner.y);
      if (distance < minDistance) {
        minDistance = distance;
        nearest = mine;
      }
    });
    
    return nearest;
  }

  manageMines() {
    for (let i = this.mines.children.length - 1; i >= 0; i--) {
      const mine = this.mines.children[i];
      if (mine.goldAmount <= 0) {
        // Depletion effect
        this.effects.createExplosionParticles(this.app.stage, {
          x: mine.x,
          y: mine.y,
          color: 0x8B4513
        });
        this.mines.removeChildAt(i);
      }
    }
    
    while (this.mines.children.length < this.maxMines) {
      this.createMine();
    }
  }

  upgradeMinerCount() {
    if (this.gold >= this.minerCost) {
      this.gold -= this.minerCost;
      this.minerCount++;
      this.createMiner();
      this.minerCost *= 2;
      this.effects.screenShake(this.app.stage);
    }
  }

  upgradeMiningSpeed() {
    if (this.gold >= this.speedCost) {
      this.gold -= this.speedCost;
      this.miningSpeed *= 1.2;
      this.speedCost *= 2;
      
      // Highlight all miners
      this.miners.children.forEach(miner => {
        this.effects.highlightCharacter(miner.sprite);
      });
    }
  }

  upgradeCarryingCapacity() {
    if (this.gold >= this.capacityCost) {
      this.gold -= this.capacityCost;
      this.carryingCapacity = Math.floor(this.carryingCapacity * 1.5);
      this.capacityCost *= 2;
      
      // Effect on depot
      this.effects.createExplosionParticles(this.app.stage, {
        x: this.depotContainer.x,
        y: this.depotContainer.y,
        color: 0x4a9eff
      });
    }
  }

  upgradeMaxMines() {
    if (this.gold >= this.maxMinesCost) {
      this.gold -= this.maxMinesCost;
      this.maxMines++;
      this.createMine();
      this.maxMinesCost *= 2;
      this.effects.screenShake(this.app.stage);
    }
  }

  upgradeMineSize() {
    if (this.gold >= this.mineSizeCost) {
      this.gold -= this.mineSizeCost;
      this.mineSize = Math.floor(this.mineSize * 1.5);
      this.mineSizeCost *= 2;
      
      // Highlight all mines
      this.mines.children.forEach(mine => {
        this.effects.highlightCharacter(mine.sprite);
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
