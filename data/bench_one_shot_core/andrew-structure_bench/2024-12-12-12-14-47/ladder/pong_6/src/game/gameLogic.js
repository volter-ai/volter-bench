import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS } from './gameData';
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

    this.effects = new EffectsLibrary(this.app);
    
    this.ready = false;
    this.score = 0;
    this.consecutiveHits = 0;
    this.lastTimestamp = performance.now();

    // Game values
    this.paddleHeight = INITIAL_VALUES.PADDLE_HEIGHT;
    this.paddleSpeed = INITIAL_VALUES.PADDLE_SPEED;
    this.ballSpeed = INITIAL_VALUES.BALL_SPEED;
    this.currentBallSpeed = INITIAL_VALUES.BALL_SPEED;
    this.pointMultiplier = INITIAL_VALUES.POINT_MULTIPLIER;
    this.paddlePrediction = INITIAL_VALUES.PADDLE_PREDICTION;
    this.comboMultiplier = INITIAL_VALUES.COMBO_MULTIPLIER;

    // Upgrade costs
    this.paddleHeightCost = UPGRADE_COSTS.PADDLE_HEIGHT;
    this.paddleSpeedCost = UPGRADE_COSTS.PADDLE_SPEED;
    this.pointMultiplierCost = UPGRADE_COSTS.POINT_MULTIPLIER;
    this.ballSpeedCost = UPGRADE_COSTS.BALL_SPEED;
    this.paddlePredictionCost = UPGRADE_COSTS.PADDLE_PREDICTION;
    this.comboMultiplierCost = UPGRADE_COSTS.COMBO_MULTIPLIER;

    this.createGameObjects();
    this.app.ticker.add(this.gameLoop.bind(this));
    this.ready = true;
  }

  createGameObjects() {
    // Create containers
    this.leftPaddleContainer = new PIXI.Container();
    this.rightPaddleContainer = new PIXI.Container();
    this.ballContainer = new PIXI.Container();

    // Create paddles
    this.leftPaddle = new PIXI.Graphics();
    this.rightPaddle = new PIXI.Graphics();
    this.updatePaddles();

    // Create ball texture
    const ballGraphics = new PIXI.Graphics();
    ballGraphics.beginFill(0xFFFFFF);
    ballGraphics.drawCircle(0, 0, INITIAL_VALUES.BALL_SIZE);
    ballGraphics.endFill();
    const ballTexture = this.app.renderer.generateTexture(ballGraphics);
    
    // Create ball sprite
    this.ball = new PIXI.Sprite(ballTexture);
    this.ball.anchor.set(0.5);
    
    // Add objects to containers
    this.leftPaddleContainer.addChild(this.leftPaddle);
    this.rightPaddleContainer.addChild(this.rightPaddle);
    this.ballContainer.addChild(this.ball);

    // Create shadows
    this.effects.createShadow(this.ballContainer, this.ball, { offsetY: 5 });
    this.effects.createShadow(this.leftPaddleContainer, this.leftPaddle, { offsetY: 5 });
    this.effects.createShadow(this.rightPaddleContainer, this.rightPaddle, { offsetY: 5 });

    // Add containers to stage
    this.app.stage.addChild(this.leftPaddleContainer);
    this.app.stage.addChild(this.rightPaddleContainer);
    this.app.stage.addChild(this.ballContainer);

    // Create particle system for ball trail
    this.ballTrail = this.effects.createParticleSystem(this.ballContainer, {
      maxParticles: 20,
      spawnInterval: 1,
      radius: 2
    });

    this.resetBall();
  }

  updatePaddles() {
    [this.leftPaddle, this.rightPaddle].forEach((paddle, index) => {
      paddle.clear();
      paddle.beginFill(0xFFFFFF);
      paddle.drawRect(0, 0, INITIAL_VALUES.PADDLE_WIDTH, this.paddleHeight);
      paddle.endFill();
      
      const container = index === 0 ? this.leftPaddleContainer : this.rightPaddleContainer;
      container.x = index === 0 ? 50 : SCREEN_SIZE.width - 50 - INITIAL_VALUES.PADDLE_WIDTH;
      container.y = SCREEN_SIZE.height / 2 - this.paddleHeight / 2;
    });
  }

  resetBall() {
    this.ballContainer.x = SCREEN_SIZE.width / 2;
    this.ballContainer.y = SCREEN_SIZE.height / 2;
    this.currentBallSpeed = this.ballSpeed;
    const angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
    this.ballContainer.vx = Math.cos(angle) * this.currentBallSpeed * (Math.random() < 0.5 ? 1 : -1);
    this.ballContainer.vy = Math.sin(angle) * this.currentBallSpeed;
    this.consecutiveHits = 0;

    this.effects.spawnAnimation(this.ballContainer);
  }

  gameLoop(delta) {
    const elapsedSecs = delta / 60;

    // Move ball
    this.ballContainer.x += this.ballContainer.vx * elapsedSecs;
    this.ballContainer.y += this.ballContainer.vy * elapsedSecs;

    // Update ball trail
    this.ballTrail.update(delta);

    // Ball collision with top/bottom
    if (this.ballContainer.y < 0 || this.ballContainer.y > SCREEN_SIZE.height) {
      this.ballContainer.vy *= -1;
      this.effects.createImpactEffect(this.app.stage, {
        x: this.ballContainer.x,
        y: this.ballContainer.y,
        color: 0x7C45CB
      });
      this.effects.screenShake(this.app.stage, { intensity: 3 });
    }

    // AI paddle movement
    [this.leftPaddleContainer, this.rightPaddleContainer].forEach(container => {
      const targetY = this.ballContainer.y - this.paddleHeight / 2 + 
        (Math.random() * 2 - 1) * (1 - this.paddlePrediction) * this.paddleHeight;
      
      const dy = targetY - container.y;
      container.y += Math.sign(dy) * this.paddleSpeed * elapsedSecs;
      container.y = Math.max(0, Math.min(SCREEN_SIZE.height - this.paddleHeight, container.y));
    });

    // Paddle collision
    [this.leftPaddleContainer, this.rightPaddleContainer].forEach(container => {
      if (this.checkPaddleCollision(container)) {
        this.currentBallSpeed *= 1.1;
        this.ballContainer.vx *= -1;
        const angleChange = (Math.random() - 0.5) * Math.PI / 4;
        const speed = Math.sqrt(this.ballContainer.vx * this.ballContainer.vx + this.ballContainer.vy * this.ballContainer.vy);
        const angle = Math.atan2(this.ballContainer.vy, this.ballContainer.vx) + angleChange;
        this.ballContainer.vx = Math.cos(angle) * speed;
        this.ballContainer.vy = Math.sin(angle) * speed;
        
        this.consecutiveHits++;
        const points = this.pointMultiplier * Math.pow(this.comboMultiplier, this.consecutiveHits - 1);
        this.score += points;

        // Collision effects
        this.effects.createImpactEffect(this.app.stage, {
          x: this.ballContainer.x,
          y: this.ballContainer.y,
          color: 0x7C45CB
        });
        this.effects.screenShake(this.app.stage, { 
          intensity: Math.min(5 + this.consecutiveHits, 15) 
        });
        this.effects.flashColor(this.ball, { color: 0x7C45CB });
        this.effects.showFloatingText(container, `+${Math.floor(points)}`);
        this.effects.lungeAnimation(container, { x: this.ballContainer.x, y: this.ballContainer.y });
      }
    });

    // Ball out of bounds
    if (this.ballContainer.x < 0 || this.ballContainer.x > SCREEN_SIZE.width) {
      this.effects.createExplosionParticles(this.app.stage, {
        x: this.ballContainer.x,
        y: this.ballContainer.y,
        color: 0x7C45CB
      });
      this.resetBall();
    }
  }

  checkPaddleCollision(container) {
    return this.ballContainer.x + INITIAL_VALUES.BALL_SIZE > container.x &&
           this.ballContainer.x - INITIAL_VALUES.BALL_SIZE < container.x + INITIAL_VALUES.PADDLE_WIDTH &&
           this.ballContainer.y + INITIAL_VALUES.BALL_SIZE > container.y &&
           this.ballContainer.y - INITIAL_VALUES.BALL_SIZE < container.y + this.paddleHeight;
  }

  upgradePaddleHeight() {
    if (this.score >= this.paddleHeightCost) {
      this.score -= this.paddleHeightCost;
      this.paddleHeight += 10;
      this.paddleHeightCost *= 2;
      this.updatePaddles();
      this.effects.createSpiralParticles(this.app.stage, {
        x: this.leftPaddleContainer.x,
        y: this.leftPaddleContainer.y + this.paddleHeight/2
      });
      this.effects.createSpiralParticles(this.app.stage, {
        x: this.rightPaddleContainer.x,
        y: this.rightPaddleContainer.y + this.paddleHeight/2
      });
    }
  }

  upgradePaddleSpeed() {
    if (this.score >= this.paddleSpeedCost) {
      this.score -= this.paddleSpeedCost;
      this.paddleSpeed *= 1.2;
      this.paddleSpeedCost *= 2;
      [this.leftPaddle, this.rightPaddle].forEach(paddle => {
        this.effects.highlightCharacter(paddle);
      });
    }
  }

  upgradePointMultiplier() {
    if (this.score >= this.pointMultiplierCost) {
      this.score -= this.pointMultiplierCost;
      this.pointMultiplier *= 1.5;
      this.pointMultiplierCost *= 2;
      this.effects.createSpiralParticles(this.app.stage, {
        x: SCREEN_SIZE.width/2,
        y: SCREEN_SIZE.height/2
      });
    }
  }

  upgradeBallSpeed() {
    if (this.score >= this.ballSpeedCost) {
      this.score -= this.ballSpeedCost;
      this.ballSpeed *= 1.2;
      this.ballSpeedCost *= 2;
      this.effects.flashColor(this.ball, { color: 0xFFFF00 });
    }
  }

  upgradePaddlePrediction() {
    if (this.score >= this.paddlePredictionCost) {
      this.score -= this.paddlePredictionCost;
      this.paddlePrediction = Math.min(1, this.paddlePrediction + 0.05);
      this.paddlePredictionCost *= 2;
      [this.leftPaddleContainer, this.rightPaddleContainer].forEach(container => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: container.x,
          y: container.y + this.paddleHeight/2
        });
      });
    }
  }

  upgradeComboMultiplier() {
    if (this.score >= this.comboMultiplierCost) {
      this.score -= this.comboMultiplierCost;
      this.comboMultiplier *= 1.2;
      this.comboMultiplierCost *= 2;
      this.effects.createSpiralParticles(this.app.stage, {
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
