import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, GAME_CONSTANTS } from './gameData';
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
    this.score = 0;
    this.lastTimestamp = performance.now();
    
    // Game attributes
    this.paddleSize = INITIAL_VALUES.PADDLE_SIZE;
    this.ballSpeed = INITIAL_VALUES.BALL_SPEED;
    this.pointsPerHit = INITIAL_VALUES.POINTS_PER_HIT;
    this.paddleSpeed = INITIAL_VALUES.PADDLE_SPEED;
    this.paddleAccuracy = INITIAL_VALUES.PADDLE_ACCURACY;

    // Upgrade costs
    this.paddleSizeCost = UPGRADE_COSTS.PADDLE_SIZE;
    this.ballSpeedCost = UPGRADE_COSTS.BALL_SPEED;
    this.pointsPerHitCost = UPGRADE_COSTS.POINTS_PER_HIT;
    this.paddleSpeedCost = UPGRADE_COSTS.PADDLE_SPEED;
    this.paddleAccuracyCost = UPGRADE_COSTS.PADDLE_ACCURACY;

    // Create basic shapes instead of loading sprites
    this.createGameObjects();
    this.app.ticker.add(this.gameLoop.bind(this));
    this.ready = true;
  }

  getSprite(spriteConfig) {
    // Instead of loading sprites, create graphics
    const graphics = new PIXI.Graphics();
    
    if (spriteConfig === SPRITES.background) {
      graphics.beginFill(0x000000);
      graphics.drawRect(0, 0, spriteConfig.width, spriteConfig.height);
      graphics.endFill();
    } else if (spriteConfig === SPRITES.paddle) {
      graphics.beginFill(0xFFFFFF);
      graphics.drawRect(-spriteConfig.width/2, -spriteConfig.height/2, spriteConfig.width, spriteConfig.height);
      graphics.endFill();
    } else if (spriteConfig === SPRITES.ball) {
      graphics.beginFill(0xFFFFFF);
      // Draw circle centered at 0,0 for easier positioning
      graphics.drawCircle(0, 0, spriteConfig.width/2);
      graphics.endFill();
    }
    
    return graphics;
  }

  createGameObjects() {
    this.background = this.getSprite(SPRITES.background);
    
    // Create paddles
    this.leftPaddle = this.getSprite(SPRITES.paddle);
    this.rightPaddle = this.getSprite(SPRITES.paddle);
    
    this.leftPaddle.x = GAME_CONSTANTS.PADDLE_EDGE_MARGIN;
    this.rightPaddle.x = SCREEN_SIZE.width - GAME_CONSTANTS.PADDLE_EDGE_MARGIN;
    
    this.leftPaddle.y = SCREEN_SIZE.height / 2;
    this.rightPaddle.y = SCREEN_SIZE.height / 2;

    // Create ball
    this.ball = this.getSprite(SPRITES.ball);
    // Remove anchor.set since we're using Graphics
    // Ball is already centered due to how we drew it
    this.resetBall();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.leftPaddle);
    this.app.stage.addChild(this.rightPaddle);
    this.app.stage.addChild(this.ball);
  }

  resetBall() {
    this.ball.x = SCREEN_SIZE.width / 2;
    this.ball.y = SCREEN_SIZE.height / 2;
    const angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
    this.ball.vx = Math.cos(angle) * this.ballSpeed * (Math.random() < 0.5 ? 1 : -1);
    this.ball.vy = Math.sin(angle) * this.ballSpeed;
  }

  gameLoop(delta) {
    if (!this.ready) return;

    const elapsedSecs = delta / 60;

    // Update paddle sizes
    this.leftPaddle.clear();
    this.rightPaddle.clear();
    this.leftPaddle.beginFill(0xFFFFFF);
    this.rightPaddle.beginFill(0xFFFFFF);
    this.leftPaddle.drawRect(-GAME_CONSTANTS.PADDLE_WIDTH/2, -this.paddleSize/2, 
                            GAME_CONSTANTS.PADDLE_WIDTH, this.paddleSize);
    this.rightPaddle.drawRect(-GAME_CONSTANTS.PADDLE_WIDTH/2, -this.paddleSize/2, 
                             GAME_CONSTANTS.PADDLE_WIDTH, this.paddleSize);
    this.leftPaddle.endFill();
    this.rightPaddle.endFill();

    // Move ball
    this.ball.x += this.ball.vx * elapsedSecs;
    this.ball.y += this.ball.vy * elapsedSecs;

    // Ball collision with top/bottom
    if (this.ball.y < 0 || this.ball.y > SCREEN_SIZE.height) {
      this.ball.vy *= -1;
    }

    // AI paddle movement
    const movePaddle = (paddle, targetY) => {
      const error = (1 - this.paddleAccuracy) * 100;
      const adjustedTargetY = targetY + (Math.random() * error * 2 - error);
      const dy = adjustedTargetY - paddle.y;
      paddle.y += Math.sign(dy) * this.paddleSpeed * elapsedSecs;
      paddle.y = Math.max(this.paddleSize/2, Math.min(SCREEN_SIZE.height - this.paddleSize/2, paddle.y));
    };

    if (this.ball.vx < 0) {
      movePaddle(this.leftPaddle, this.ball.y);
    } else {
      movePaddle(this.rightPaddle, this.ball.y);
    }

    // Ball collision with paddles
    const checkPaddleCollision = (paddle) => {
      if (this.ball.x > paddle.x - GAME_CONSTANTS.PADDLE_WIDTH/2 && 
          this.ball.x < paddle.x + GAME_CONSTANTS.PADDLE_WIDTH/2 &&
          this.ball.y > paddle.y - this.paddleSize/2 &&
          this.ball.y < paddle.y + this.paddleSize/2) {
        this.ball.vx *= -1;
        this.score += this.pointsPerHit;
      }
    };

    checkPaddleCollision(this.leftPaddle);
    checkPaddleCollision(this.rightPaddle);

    // Reset ball if it goes past paddles
    if (this.ball.x < 0 || this.ball.x > SCREEN_SIZE.width) {
      this.resetBall();
    }
  }

  upgradePaddleSize() {
    if (this.score >= this.paddleSizeCost) {
      this.score -= this.paddleSizeCost;
      this.paddleSize += 10;
      this.paddleSizeCost *= 2;
    }
  }

  upgradeBallSpeed() {
    if (this.score >= this.ballSpeedCost) {
      this.score -= this.ballSpeedCost;
      this.ballSpeed += 50;
      this.ballSpeedCost *= 2;
    }
  }

  upgradePointsPerHit() {
    if (this.score >= this.pointsPerHitCost) {
      this.score -= this.pointsPerHitCost;
      this.pointsPerHit += 1;
      this.pointsPerHitCost *= 2;
    }
  }

  upgradePaddleSpeed() {
    if (this.score >= this.paddleSpeedCost) {
      this.score -= this.paddleSpeedCost;
      this.paddleSpeed += 50;
      this.paddleSpeedCost *= 2;
    }
  }

  upgradePaddleAccuracy() {
    if (this.score >= this.paddleAccuracyCost) {
      this.score -= this.paddleAccuracyCost;
      this.paddleAccuracy = Math.min(1, this.paddleAccuracy + 0.05);
      this.paddleAccuracyCost *= 2;
    }
  }

  destroy() {
    this.app.destroy(true);
  }
}
