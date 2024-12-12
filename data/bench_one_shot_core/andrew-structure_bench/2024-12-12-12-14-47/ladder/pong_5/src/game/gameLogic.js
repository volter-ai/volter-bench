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

    this.effects = new EffectsLibrary(this.app);
    this.ready = false;
    this.score = 0;
    this.lastTimestamp = performance.now();
    
    // Game attributes
    this.ballSpeed = INITIAL_VALUES.BALL_SPEED;
    this.paddleSize = INITIAL_VALUES.PADDLE_SIZE;
    this.ballCount = INITIAL_VALUES.BALL_COUNT;
    this.paddleSpeed = INITIAL_VALUES.PADDLE_SPEED;
    this.pointsPerHit = INITIAL_VALUES.POINTS_PER_HIT;

    // Upgrade costs
    this.ballSpeedCost = UPGRADE_COSTS.BALL_SPEED;
    this.paddleSizeCost = UPGRADE_COSTS.PADDLE_SIZE;
    this.ballCountCost = UPGRADE_COSTS.BALL_COUNT;
    this.paddleSpeedCost = UPGRADE_COSTS.PADDLE_SPEED;
    this.pointsPerHitCost = UPGRADE_COSTS.POINTS_PER_HIT;

    loadAssets(SPRITES, () => {
      if (!this.app.stage) return;
      this.createGameObjects();
      this.app.ticker.add(this.gameLoop.bind(this));
      this.ready = true;
    });
  }

  getSprite(name) {
    const sprite = new PIXI.Sprite(PIXI.Loader.shared.resources[name].texture);
    sprite.width = SPRITES[name].width;
    sprite.height = SPRITES[name].height;
    return sprite;
  }

  createGameObjects() {
    this.background = this.getSprite('background');
    
    // Create paddle containers
    this.leftPaddle = new PIXI.Container();
    this.rightPaddle = new PIXI.Container();
    
    const leftPaddleSprite = this.getSprite('paddle');
    const rightPaddleSprite = this.getSprite('paddle');
    
    // Store sprite references
    this.leftPaddle.sprite = leftPaddleSprite;
    this.rightPaddle.sprite = rightPaddleSprite;
    
    leftPaddleSprite.anchor.set(0.5);
    rightPaddleSprite.anchor.set(0.5);
    
    this.leftPaddle.addChild(leftPaddleSprite);
    this.rightPaddle.addChild(rightPaddleSprite);
    
    this.leftPaddle.x = GAME_CONFIG.PADDLE_OFFSET;
    this.rightPaddle.x = SCREEN_SIZE.width - GAME_CONFIG.PADDLE_OFFSET;
    
    this.leftPaddle.y = SCREEN_SIZE.height / 2;
    this.rightPaddle.y = SCREEN_SIZE.height / 2;

    // Add shadows to paddles
    this.effects.createShadow(this.leftPaddle, leftPaddleSprite);
    this.effects.createShadow(this.rightPaddle, rightPaddleSprite);
    
    // Add idle animations
    this.effects.idleAnimation(this.leftPaddle);
    this.effects.idleAnimation(this.rightPaddle);

    // Create balls container
    this.balls = new PIXI.Container();
    this.createBall();

    this.app.stage.addChild(this.background);
    this.app.stage.addChild(this.leftPaddle);
    this.app.stage.addChild(this.rightPaddle);
    this.app.stage.addChild(this.balls);
  }

  createBall() {
    const ballContainer = new PIXI.Container();
    const ballSprite = this.getSprite('ball');
    ballSprite.anchor.set(0.5);
    
    // Store sprite reference
    ballContainer.sprite = ballSprite;
    
    // Add glow/border effect
    const borderedBall = this.effects.createSpriteBorder(ballSprite.texture, {
      borderProportion: 0.2,
      color: 0x00FFFF
    });
    
    ballContainer.addChild(borderedBall);
    
    // Add particle trail
    const particleSystem = this.effects.createParticleSystem(ballContainer, {
      maxParticles: 20,
      spawnInterval: 2,
      radius: 2
    });
    
    this.resetBall(ballContainer);
    this.balls.addChild(ballContainer);
    
    // Spawn animation
    this.effects.spawnAnimation(ballContainer);
    this.effects.createSpiralParticles(this.app.stage, {
      x: ballContainer.x,
      y: ballContainer.y
    });
  }

  resetBall(ball) {
    ball.x = SCREEN_SIZE.width / 2;
    ball.y = SCREEN_SIZE.height / 2;
    const angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
    ball.dx = Math.cos(angle) * this.ballSpeed * (Math.random() < 0.5 ? 1 : -1);
    ball.dy = Math.sin(angle) * this.ballSpeed;
  }

  gameLoop(delta) {
    const currentTimestamp = performance.now();
    const elapsedSecs = (currentTimestamp - this.lastTimestamp) / 1000;
    this.lastTimestamp = currentTimestamp;

    // Update paddle sizes
    this.leftPaddle.children[0].height = this.paddleSize;
    this.rightPaddle.children[0].height = this.paddleSize;

    // AI paddle movement
    this.movePaddles(elapsedSecs);
    this.moveBalls(elapsedSecs);
  }

  movePaddles(elapsedSecs) {
    [this.leftPaddle, this.rightPaddle].forEach(paddle => {
      let closestBall = null;
      let closestDist = Infinity;
      
      this.balls.children.forEach(ball => {
        const dist = Math.abs(ball.x - paddle.x);
        if (dist < closestDist) {
          closestDist = dist;
          closestBall = ball;
        }
      });

      if (closestBall) {
        const prevY = paddle.y;
        const targetY = closestBall.y;
        const dy = targetY - paddle.y;
        const movement = Math.min(Math.abs(dy), this.paddleSpeed * elapsedSecs) * Math.sign(dy);
        paddle.y += movement;
        
        // Add movement particles if moving fast
        if (Math.abs(paddle.y - prevY) > 5) {
          this.effects.createParticleSystem(paddle, {
            maxParticles: 10,
            spawnInterval: 5
          });
        }
      }

      paddle.y = Math.max(paddle.height/2, Math.min(SCREEN_SIZE.height - paddle.height/2, paddle.y));
    });
  }

  moveBalls(elapsedSecs) {
    this.balls.children.forEach(ball => {
      ball.x += ball.dx * elapsedSecs;
      ball.y += ball.dy * elapsedSecs;

      if (ball.y < 0 || ball.y > SCREEN_SIZE.height) {
        ball.dy *= -1;
        this.effects.createImpactEffect(this.app.stage, {
          x: ball.x,
          y: ball.y,
          color: 0x00FFFF
        });
      }

      [this.leftPaddle, this.rightPaddle].forEach(paddle => {
        if (this.checkPaddleCollision(ball, paddle)) {
          const paddleCenter = paddle.y;
          const relativeIntersectY = paddleCenter - ball.y;
          const normalizedIntersectY = relativeIntersectY / (paddle.height / 2);
          const bounceAngle = normalizedIntersectY * Math.PI / 4;
          
          const direction = paddle === this.leftPaddle ? 1 : -1;
          ball.dx = this.ballSpeed * Math.cos(bounceAngle) * direction;
          ball.dy = -this.ballSpeed * Math.sin(bounceAngle);
          
          // Collision effects
          this.effects.createImpactEffect(this.app.stage, {
            x: ball.x,
            y: ball.y
          });
          this.effects.createExplosionParticles(this.app.stage, {
            x: ball.x,
            y: ball.y,
            count: 20
          });
          // Use stored sprite reference
          this.effects.flashColor(paddle.sprite, {
            color: 0x00FFFF
          });
          this.effects.screenShake(this.app.stage, {
            intensity: 5,
            duration: 0.2
          });
          
          // Score effects
          this.score += this.pointsPerHit;
          this.effects.showFloatingText(paddle, `+${this.pointsPerHit}`, {
            color: 0x00FFFF
          });
          this.effects.highlightCharacter(paddle.sprite);
        }
      });

      if (ball.x < 0 || ball.x > SCREEN_SIZE.width) {
        this.resetBall(ball);
        this.effects.createSpiralParticles(this.app.stage, {
          x: ball.x,
          y: ball.y
        });
      }
    });
  }

  checkPaddleCollision(ball, paddle) {
    return ball.x + ball.width/2 > paddle.x - paddle.width/2 &&
           ball.x - ball.width/2 < paddle.x + paddle.width/2 &&
           ball.y + ball.height/2 > paddle.y - paddle.height/2 &&
           ball.y - ball.height/2 < paddle.y + paddle.height/2;
  }

  upgradeBallSpeed() {
    if (this.score >= this.ballSpeedCost) {
      this.score -= this.ballSpeedCost;
      this.ballSpeed *= 1.1;
      this.ballSpeedCost *= 2;
      this.balls.children.forEach(ball => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: ball.x,
          y: ball.y,
          color: 0xFFFF00
        });
      });
    }
  }

  upgradePaddleSize() {
    if (this.score >= this.paddleSizeCost) {
      this.score -= this.paddleSizeCost;
      this.paddleSize *= 1.2;
      this.paddleSizeCost *= 2;
      [this.leftPaddle, this.rightPaddle].forEach(paddle => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: paddle.x,
          y: paddle.y,
          color: 0xFFFF00
        });
      });
    }
  }

  addBall() {
    if (this.score >= this.ballCountCost) {
      this.score -= this.ballCountCost;
      this.ballCount++;
      this.createBall();
      this.ballCountCost *= 2;
      this.effects.screenShake(this.app.stage, {
        intensity: 8,
        duration: 0.3
      });
    }
  }

  upgradePaddleSpeed() {
    if (this.score >= this.paddleSpeedCost) {
      this.score -= this.paddleSpeedCost;
      this.paddleSpeed *= 1.2;
      this.paddleSpeedCost *= 2;
      [this.leftPaddle, this.rightPaddle].forEach(paddle => {
        this.effects.createSpiralParticles(this.app.stage, {
          x: paddle.x,
          y: paddle.y,
          color: 0xFFFF00
        });
      });
    }
  }

  upgradePointsPerHit() {
    if (this.score >= this.pointsPerHitCost) {
      this.score -= this.pointsPerHitCost;
      this.pointsPerHit++;
      this.pointsPerHitCost *= 2;
      this.effects.screenShake(this.app.stage, {
        intensity: 5,
        duration: 0.2
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
