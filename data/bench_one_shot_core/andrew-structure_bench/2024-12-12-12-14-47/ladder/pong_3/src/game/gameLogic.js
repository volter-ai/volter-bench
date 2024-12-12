import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS } from './gameData';
import { SPRITES } from './assetManifest';

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
    this.ballSpeed = INITIAL_VALUES.BALL_SPEED;
    this.paddleSize = INITIAL_VALUES.PADDLE_SIZE;
    this.ballCount = INITIAL_VALUES.BALL_COUNT;
    this.paddleSpeed = INITIAL_VALUES.PADDLE_SPEED;
    this.pointsMultiplier = INITIAL_VALUES.POINTS_MULTIPLIER;

    this.ballSpeedCost = UPGRADE_COSTS.BALL_SPEED;
    this.paddleSizeCost = UPGRADE_COSTS.PADDLE_SIZE;
    this.ballCountCost = UPGRADE_COSTS.BALL_COUNT;
    this.paddleSpeedCost = UPGRADE_COSTS.PADDLE_SPEED;
    this.pointsMultiplierCost = UPGRADE_COSTS.POINTS_MULTIPLIER;

    // Instead of using loadAssets, we'll load directly
    this.createGameObjects();
    this.app.ticker.add(this.gameLoop.bind(this));
    this.ready = true;
  }

  getSprite(spriteConfig) {
    // Create a simple colored rectangle instead of loading sprites
    const graphics = new PIXI.Graphics();
    if (spriteConfig === SPRITES.background) {
      graphics.beginFill(0x222C37);
      graphics.drawRect(0, 0, spriteConfig.width, spriteConfig.height);
    } else if (spriteConfig === SPRITES.paddle) {
      graphics.beginFill(0xFFFFFF);
      graphics.drawRect(-spriteConfig.width/2, -spriteConfig.height/2, spriteConfig.width, spriteConfig.height);
    } else if (spriteConfig === SPRITES.ball) {
      graphics.beginFill(0xFFFFFF);
      graphics.drawCircle(0, 0, spriteConfig.width/2);
    }
    graphics.endFill();
    return graphics;
  }

  // Rest of the GameLogic class remains exactly the same
  createGameObjects() {
    this.background = this.getSprite(SPRITES.background);
    
    this.paddles = new PIXI.Container();
    this.leftPaddle = this.getSprite(SPRITES.paddle);
    this.rightPaddle = this.getSprite(SPRITES.paddle);
    
    this.leftPaddle.x = 50;
    this.rightPaddle.x = SCREEN_SIZE.width - 70;
    this.leftPaddle.y = SCREEN_SIZE.height / 2;
    this.rightPaddle.y = SCREEN_SIZE.height / 2;
    
    this.paddles.addChild(this.leftPaddle);
    this.paddles.addChild(this.rightPaddle);

    this.balls = new PIXI.Container();
    this.createBall();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.paddles);
    this.app.stage.addChild(this.balls);
  }

  createBall() {
    const ball = this.getSprite(SPRITES.ball);
    ball.x = SCREEN_SIZE.width / 2;
    ball.y = SCREEN_SIZE.height / 2;
    const angle = (Math.random() * Math.PI/2) - Math.PI/4;
    ball.dx = Math.cos(angle) * this.ballSpeed * (Math.random() < 0.5 ? 1 : -1);
    ball.dy = Math.sin(angle) * this.ballSpeed;
    this.balls.addChild(ball);
  }

  gameLoop(delta) {
    const elapsedSecs = delta / 60;
    this.movePaddles(elapsedSecs);
    this.moveBalls(elapsedSecs);
  }

  movePaddles(elapsedSecs) {
    [this.leftPaddle, this.rightPaddle].forEach(paddle => {
      let nearestBall = null;
      let nearestDist = Infinity;
      
      this.balls.children.forEach(ball => {
        const dist = Math.abs(ball.y - paddle.y);
        if (dist < nearestDist) {
          nearestDist = dist;
          nearestBall = ball;
        }
      });

      if (nearestBall) {
        const moveDir = nearestBall.y > paddle.y ? 1 : -1;
        paddle.y += moveDir * this.paddleSpeed * elapsedSecs;
      }

      paddle.y = Math.max(this.paddleSize/2, Math.min(SCREEN_SIZE.height - this.paddleSize/2, paddle.y));
      paddle.height = this.paddleSize;
    });
  }

  moveBalls(elapsedSecs) {
    this.balls.children.forEach(ball => {
      ball.x += ball.dx * elapsedSecs;
      ball.y += ball.dy * elapsedSecs;

      if (ball.y < 0 || ball.y > SCREEN_SIZE.height) {
        ball.dy *= -1;
      }

      [this.leftPaddle, this.rightPaddle].forEach(paddle => {
        if (this.checkCollision(ball, paddle)) {
          ball.dx *= -1;
          this.score += this.pointsMultiplier;
        }
      });

      if (ball.x < 0 || ball.x > SCREEN_SIZE.width) {
        ball.x = SCREEN_SIZE.width / 2;
        ball.y = SCREEN_SIZE.height / 2;
        const angle = (Math.random() * Math.PI/2) - Math.PI/4;
        ball.dx = Math.cos(angle) * this.ballSpeed * (Math.random() < 0.5 ? 1 : -1);
        ball.dy = Math.sin(angle) * this.ballSpeed;
      }
    });

    while (this.balls.children.length < this.ballCount) {
      this.createBall();
    }
  }

  checkCollision(ball, paddle) {
    return ball.x > paddle.x - paddle.width/2 &&
           ball.x < paddle.x + paddle.width/2 &&
           ball.y > paddle.y - paddle.height/2 &&
           ball.y < paddle.y + paddle.height/2;
  }

  upgradeBallSpeed() {
    if (this.score >= this.ballSpeedCost) {
      this.score -= this.ballSpeedCost;
      this.ballSpeed *= 1.1;
      this.ballSpeedCost *= 2;
    }
  }

  upgradePaddleSize() {
    if (this.score >= this.paddleSizeCost) {
      this.score -= this.paddleSizeCost;
      this.paddleSize *= 1.1;
      this.paddleSizeCost *= 2;
    }
  }

  upgradeBallCount() {
    if (this.score >= this.ballCountCost) {
      this.score -= this.ballCountCost;
      this.ballCount += 1;
      this.ballCountCost *= 2;
    }
  }

  upgradePaddleSpeed() {
    if (this.score >= this.paddleSpeedCost) {
      this.score -= this.paddleSpeedCost;
      this.paddleSpeed *= 1.1;
      this.paddleSpeedCost *= 2;
    }
  }

  upgradePointsMultiplier() {
    if (this.score >= this.pointsMultiplierCost) {
      this.score -= this.pointsMultiplierCost;
      this.pointsMultiplier *= 1.1;
      this.pointsMultiplierCost *= 2;
    }
  }

  destroy() {
    this.app.destroy(true);
  }
}
