import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, GAME_CONFIG } from './gameData';
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
    this.score = 0;
    this.lastTimestamp = performance.now();
    
    // Game values
    this.paddleHeight = INITIAL_VALUES.PADDLE_HEIGHT;
    this.paddleSpeed = INITIAL_VALUES.PADDLE_SPEED;
    this.pointMultiplier = INITIAL_VALUES.POINT_MULTIPLIER;
    this.ballSpeed = INITIAL_VALUES.BALL_SPEED;
    this.currentBallSpeed = INITIAL_VALUES.BALL_SPEED;
    this.speedScaling = INITIAL_VALUES.SPEED_SCALING;

    // Upgrade costs
    this.paddleHeightCost = UPGRADE_COSTS.PADDLE_HEIGHT;
    this.paddleSpeedCost = UPGRADE_COSTS.PADDLE_SPEED;
    this.pointMultiplierCost = UPGRADE_COSTS.POINT_MULTIPLIER;
    this.ballSpeedCost = UPGRADE_COSTS.BALL_SPEED;
    this.speedScalingCost = UPGRADE_COSTS.SPEED_SCALING;

    this.createGameObjects();
    this.app.ticker.add(this.gameLoop.bind(this));
    this.ready = true;
  }

  createGameObjects() {
    // Create paddle containers
    this.leftPaddle = new PIXI.Container();
    this.rightPaddle = new PIXI.Container();

    // Create paddle graphics
    const leftPaddleGraphics = new PIXI.Graphics();
    leftPaddleGraphics.beginFill(0xFFFFFF);
    leftPaddleGraphics.drawRect(0, 0, GAME_CONFIG.PADDLE_WIDTH, this.paddleHeight);
    leftPaddleGraphics.endFill();

    const rightPaddleGraphics = new PIXI.Graphics();
    rightPaddleGraphics.beginFill(0xFFFFFF);
    rightPaddleGraphics.drawRect(0, 0, GAME_CONFIG.PADDLE_WIDTH, this.paddleHeight);
    rightPaddleGraphics.endFill();

    this.leftPaddle.addChild(leftPaddleGraphics);
    this.rightPaddle.addChild(rightPaddleGraphics);

    this.leftPaddle.x = GAME_CONFIG.PADDLE_EDGE_MARGIN;
    this.leftPaddle.y = SCREEN_SIZE.height / 2 - this.paddleHeight / 2;
    this.rightPaddle.x = SCREEN_SIZE.width - GAME_CONFIG.PADDLE_EDGE_MARGIN - GAME_CONFIG.PADDLE_WIDTH;
    this.rightPaddle.y = SCREEN_SIZE.height / 2 - this.paddleHeight / 2;

    // Create ball container
    this.ballContainer = new PIXI.Container();
    
    // Create ball graphics
    this.ball = new PIXI.Graphics();
    this.ball.beginFill(0xFFFFFF);
    this.ball.drawCircle(0, 0, GAME_CONFIG.BALL_SIZE / 2);
    this.ball.endFill();
    
    this.ballContainer.addChild(this.ball);

    // Create shadows with explicit dimensions
    this.effects.createShadow(this.leftPaddle, {
      width: GAME_CONFIG.PADDLE_WIDTH,
      height: this.paddleHeight
    });
    this.effects.createShadow(this.rightPaddle, {
      width: GAME_CONFIG.PADDLE_WIDTH,
      height: this.paddleHeight
    });
    this.effects.createShadow(this.ballContainer, {
      width: GAME_CONFIG.BALL_SIZE,
      height: GAME_CONFIG.BALL_SIZE
    });

    // Add idle animations
    this.effects.idleAnimation(this.leftPaddle);
    this.effects.idleAnimation(this.rightPaddle);

    this.resetBall();

    this.app.stage.addChild(this.leftPaddle);
    this.app.stage.addChild(this.rightPaddle);
    this.app.stage.addChild(this.ballContainer);

    // Create particle systems for paddles
    this.leftPaddleParticles = this.effects.createParticleSystem(this.leftPaddle);
    this.rightPaddleParticles = this.effects.createParticleSystem(this.rightPaddle);
  }

  resetBall() {
    this.ballContainer.x = SCREEN_SIZE.width / 2;
    this.ballContainer.y = SCREEN_SIZE.height / 2;
    this.currentBallSpeed = this.ballSpeed;
    const angle = (Math.random() - 0.5) * Math.PI / 2;
    this.ballContainer.vx = Math.cos(angle) * this.currentBallSpeed * (Math.random() < 0.5 ? 1 : -1);
    this.ballContainer.vy = Math.sin(angle) * this.currentBallSpeed;

    // Spawn animation
    this.effects.spawnAnimation(this.ballContainer);
    this.effects.createSpiralParticles(this.app.stage, {
      x: this.ballContainer.x,
      y: this.ballContainer.y
    });
  }

  gameLoop() {
    const currentTime = performance.now();
    const elapsedSecs = (currentTime - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTime;

    // Move paddles towards ball
    this.movePaddle(this.leftPaddle, elapsedSecs);
    this.movePaddle(this.rightPaddle, elapsedSecs);

    // Move ball
    this.ballContainer.x += this.ballContainer.vx * elapsedSecs;
    this.ballContainer.y += this.ballContainer.vy * elapsedSecs;

    // Ball collision with top/bottom
    if (this.ballContainer.y < 0 || this.ballContainer.y > SCREEN_SIZE.height) {
      this.ballContainer.vy *= -1;
      
      // Wall collision effects
      this.effects.createImpactEffect(this.app.stage, {
        x: this.ballContainer.x,
        y: this.ballContainer.y,
        color: 0x4444FF
      });
      this.effects.screenShake(this.app.stage, { intensity: 3 });
    }

    // Ball collision with paddles
    if (this.checkPaddleCollision(this.leftPaddle) || this.checkPaddleCollision(this.rightPaddle)) {
      const hitPaddle = this.checkPaddleCollision(this.leftPaddle) ? this.leftPaddle : this.rightPaddle;
      
      this.ballContainer.vx *= -1;
      this.currentBallSpeed *= this.speedScaling;
      const speed = Math.sqrt(this.ballContainer.vx * this.ballContainer.vx + this.ballContainer.vy * this.ballContainer.vy);
      this.ballContainer.vx = (this.ballContainer.vx / speed) * this.currentBallSpeed;
      this.ballContainer.vy = (this.ballContainer.vy / speed) * this.currentBallSpeed;
      
      // Add score based on current ball speed
      const points = Math.floor(this.currentBallSpeed / 100) * this.pointMultiplier;
      this.score += points;

      // Collision effects
      this.effects.createImpactEffect(this.app.stage, {
        x: this.ballContainer.x,
        y: this.ballContainer.y
      });
      this.effects.screenShake(this.app.stage, { intensity: 5 });
      
      // Instead of flash effect, temporarily change the tint of the paddle
      const paddleGraphics = hitPaddle.children[0];
      const originalTint = paddleGraphics.tint;
      paddleGraphics.tint = 0xFFFFFF;
      setTimeout(() => {
        paddleGraphics.tint = originalTint;
      }, 100);
      
      this.effects.showFloatingText(hitPaddle, `+${points}`);
      this.effects.createExplosionParticles(this.app.stage, {
        x: this.ballContainer.x,
        y: this.ballContainer.y,
        color: 0xFFFFFF
      });
    }

    // Reset if ball goes past paddle
    if (this.ballContainer.x < 0 || this.ballContainer.x > SCREEN_SIZE.width) {
      this.resetBall();
    }
  }

  movePaddle(paddle, elapsedSecs) {
    const paddleCenter = paddle.y + this.paddleHeight / 2;
    if (Math.abs(paddleCenter - this.ballContainer.y) > 5) {
      const direction = this.ballContainer.y > paddleCenter ? 1 : -1;
      paddle.y += direction * this.paddleSpeed * elapsedSecs;
    }
    paddle.y = Math.max(0, Math.min(SCREEN_SIZE.height - this.paddleHeight, paddle.y));
  }

  checkPaddleCollision(paddle) {
    return this.ballContainer.x >= paddle.x && 
           this.ballContainer.x <= paddle.x + GAME_CONFIG.PADDLE_WIDTH &&
           this.ballContainer.y >= paddle.y && 
           this.ballContainer.y <= paddle.y + this.paddleHeight;
  }

  upgradePaddleHeight() {
    if (this.score >= this.paddleHeightCost) {
      this.score -= this.paddleHeightCost;
      this.paddleHeight += 10;
      this.paddleHeightCost *= 2;

      // Recreate paddles with new height
      this.leftPaddle.removeChildren();
      this.rightPaddle.removeChildren();

      const leftPaddleGraphics = new PIXI.Graphics();
      const rightPaddleGraphics = new PIXI.Graphics();
      
      leftPaddleGraphics.beginFill(0xFFFFFF);
      rightPaddleGraphics.beginFill(0xFFFFFF);
      leftPaddleGraphics.drawRect(0, 0, GAME_CONFIG.PADDLE_WIDTH, this.paddleHeight);
      rightPaddleGraphics.drawRect(0, 0, GAME_CONFIG.PADDLE_WIDTH, this.paddleHeight);
      leftPaddleGraphics.endFill();
      rightPaddleGraphics.endFill();

      this.leftPaddle.addChild(leftPaddleGraphics);
      this.rightPaddle.addChild(rightPaddleGraphics);

      // Upgrade effects
      this.effects.createSpiralParticles(this.app.stage, {
        x: this.leftPaddle.x,
        y: this.leftPaddle.y + this.paddleHeight/2
      });
      this.effects.createSpiralParticles(this.app.stage, {
        x: this.rightPaddle.x,
        y: this.rightPaddle.y + this.paddleHeight/2
      });
    }
  }

  upgradePaddleSpeed() {
    if (this.score >= this.paddleSpeedCost) {
      this.score -= this.paddleSpeedCost;
      this.paddleSpeed += 50;
      this.paddleSpeedCost *= 2;

      // Upgrade effects
      this.effects.createSpiralParticles(this.app.stage, {
        x: this.leftPaddle.x,
        y: this.leftPaddle.y + this.paddleHeight/2
      });
      this.effects.createSpiralParticles(this.app.stage, {
        x: this.rightPaddle.x,
        y: this.rightPaddle.y + this.paddleHeight/2
      });
    }
  }

  upgradePointMultiplier() {
    if (this.score >= this.pointMultiplierCost) {
      this.score -= this.pointMultiplierCost;
      this.pointMultiplier += 1;
      this.pointMultiplierCost *= 2;

      // Upgrade effects
      this.effects.createSpiralParticles(this.app.stage, {
        x: SCREEN_SIZE.width/2,
        y: SCREEN_SIZE.height/2,
        color: 0xFFD700
      });
    }
  }

  upgradeBallSpeed() {
    if (this.score >= this.ballSpeedCost) {
      this.score -= this.ballSpeedCost;
      this.ballSpeed += 50;
      this.ballSpeedCost *= 2;

      // Upgrade effects
      this.effects.createExplosionParticles(this.app.stage, {
        x: this.ballContainer.x,
        y: this.ballContainer.y,
        color: 0xFF4444
      });
    }
  }

  upgradeSpeedScaling() {
    if (this.score >= this.speedScalingCost) {
      this.score -= this.speedScalingCost;
      this.speedScaling += 0.1;
      this.speedScalingCost *= 2;

      // Upgrade effects
      this.effects.createSpiralParticles(this.app.stage, {
        x: this.ballContainer.x,
        y: this.ballContainer.y,
        color: 0x44FF44
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
