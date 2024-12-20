import * as PIXI from 'pixi.js';
import { INITIAL_VALUES, UPGRADE_COSTS, GAME_CONFIG } from './gameData';
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
    this.score = 0;
    this.paddleSize = INITIAL_VALUES.PADDLE_SIZE;
    this.ballSpeed = INITIAL_VALUES.BALL_SPEED;
    this.paddleSpeed = INITIAL_VALUES.PADDLE_SPEED;
    this.pointsMultiplier = INITIAL_VALUES.POINTS_MULTIPLIER;
    this.ballCount = INITIAL_VALUES.BALL_COUNT;

    this.paddleSizeCost = UPGRADE_COSTS.PADDLE_SIZE;
    this.ballSpeedCost = UPGRADE_COSTS.BALL_SPEED;
    this.multiBallCost = UPGRADE_COSTS.MULTI_BALL;
    this.pointsMultiplierCost = UPGRADE_COSTS.POINTS_MULTIPLIER;
    this.paddleSpeedCost = UPGRADE_COSTS.PADDLE_SPEED;

    // Create containers first
    this.paddles = new PIXI.Container();
    this.balls = new PIXI.Container();
    this.effectsContainer = new PIXI.Container();
    
    this.app.stage.addChild(this.paddles);
    this.app.stage.addChild(this.balls);
    this.app.stage.addChild(this.effectsContainer);

    // Load assets
    const loader = new PIXI.Loader();
    Object.values(SPRITES).forEach(sprite => {
      loader.add(sprite.path, sprite.path);
    });

    loader.load(() => {
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
    this.app.stage.addChildAt(this.background, 0);
    
    // Create left paddle container
    this.leftPaddle = new PIXI.Container();
    const leftPaddleSprite = this.getSprite(SPRITES.paddle);
    leftPaddleSprite.anchor.set(0.5);
    this.leftPaddle.addChild(leftPaddleSprite);
    this.leftPaddle.x = 50;
    this.leftPaddle.y = SCREEN_SIZE.height / 2;
    this.leftPaddle.height = this.paddleSize;
    this.leftPaddle.sprite = leftPaddleSprite; // Store sprite reference
    
    // Create right paddle container
    this.rightPaddle = new PIXI.Container();
    const rightPaddleSprite = this.getSprite(SPRITES.paddle);
    rightPaddleSprite.anchor.set(0.5);
    this.rightPaddle.addChild(rightPaddleSprite);
    this.rightPaddle.x = SCREEN_SIZE.width - 50;
    this.rightPaddle.y = SCREEN_SIZE.height / 2;
    this.rightPaddle.height = this.paddleSize;
    this.rightPaddle.sprite = rightPaddleSprite; // Store sprite reference

    // Add shadows to paddles
    this.effects.createShadow(this.leftPaddle, leftPaddleSprite);
    this.effects.createShadow(this.rightPaddle, rightPaddleSprite);

    // Add idle animations to paddles
    this.effects.idleAnimation(this.leftPaddle);
    this.effects.idleAnimation(this.rightPaddle);

    this.paddles.addChild(this.leftPaddle);
    this.paddles.addChild(this.rightPaddle);

    this.createBall();
  }

  createBall() {
    const ballContainer = new PIXI.Container();
    const ballSprite = this.getSprite(SPRITES.ball);
    ballSprite.anchor.set(0.5);
    ballContainer.addChild(ballSprite);
    ballContainer.sprite = ballSprite; // Store sprite reference
    
    // Add shadow to ball
    this.effects.createShadow(ballContainer, ballSprite, { 
      widthRatio: 0.6,
      heightRatio: 0.2
    });

    this.resetBall(ballContainer);
    ballContainer.currentSpeed = this.ballSpeed;
    this.balls.addChild(ballContainer);

    // Spawn animation
    this.effects.spawnAnimation(ballContainer);
    this.effects.createSpiralParticles(this.effectsContainer, {
      x: ballContainer.x,
      y: ballContainer.y
    });
  }

  resetBall(ball) {
    ball.x = SCREEN_SIZE.width / 2;
    ball.y = SCREEN_SIZE.height / 2;
    const angle = (Math.random() * Math.PI / 2) - Math.PI / 4;
    ball.dx = Math.cos(angle) * (Math.random() < 0.5 ? 1 : -1);
    ball.dy = Math.sin(angle);
    ball.currentSpeed = this.ballSpeed;
  }

  gameLoop(delta) {
    const elapsedSecs = delta / 60;
    
    // Move paddles
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
        const targetY = nearestBall.y;
        const dy = targetY - paddle.y;
        const moveAmount = Math.min(Math.abs(dy), this.paddleSpeed * elapsedSecs);
        paddle.y += Math.sign(dy) * moveAmount;
      }

      paddle.y = Math.max(paddle.height/2, Math.min(SCREEN_SIZE.height - paddle.height/2, paddle.y));
    });

    // Move balls
    this.balls.children.forEach(ball => {
      ball.x += ball.dx * ball.currentSpeed * elapsedSecs;
      ball.y += ball.dy * ball.currentSpeed * elapsedSecs;

      // Bounce off top/bottom
      if (ball.y < 0 || ball.y > SCREEN_SIZE.height) {
        ball.dy *= -1;
        this.effects.createImpactEffect(this.effectsContainer, {
          x: ball.x,
          y: ball.y > SCREEN_SIZE.height ? SCREEN_SIZE.height : 0
        });
      }

      // Check paddle collisions
      [this.leftPaddle, this.rightPaddle].forEach(paddle => {
        if (this.checkCollision(ball, paddle)) {
          ball.dx *= -1;
          ball.currentSpeed *= GAME_CONFIG.BALL_ACCELERATION;
          
          // Collision effects
          this.effects.createImpactEffect(this.effectsContainer, {
            x: ball.x,
            y: ball.y
          });
          this.effects.screenShake(this.app.stage, { intensity: 5 });
          this.effects.flashColor(paddle.sprite, { color: 0x7C45CB }); // Use stored sprite reference
          this.effects.createExplosionParticles(this.effectsContainer, {
            x: ball.x,
            y: ball.y,
            color: 0x7C45CB
          });
          
          // Score effects
          const points = GAME_CONFIG.BASE_POINTS * this.pointsMultiplier;
          this.score += points;
          this.effects.showFloatingText(paddle, `+${points}`, {
            color: 0x7C45CB
          });
        }
      });

      // Score/Reset
      if (ball.x < 0 || ball.x > SCREEN_SIZE.width) {
        this.resetBall(ball);
        this.effects.createSpiralParticles(this.effectsContainer, {
          x: ball.x,
          y: ball.y
        });
      }
    });
  }

  checkCollision(ball, paddle) {
    return ball.x > paddle.x - paddle.width/2 &&
           ball.x < paddle.x + paddle.width/2 &&
           ball.y > paddle.y - paddle.height/2 &&
           ball.y < paddle.y + paddle.height/2;
  }

  upgradePaddleSize() {
    if (this.score >= this.paddleSizeCost) {
      this.score -= this.paddleSizeCost;
      this.paddleSize += 20;
      this.leftPaddle.height = this.paddleSize;
      this.rightPaddle.height = this.paddleSize;
      this.paddleSizeCost *= 2;
      
      // Upgrade effects
      [this.leftPaddle, this.rightPaddle].forEach(paddle => {
        this.effects.highlightCharacter(paddle.sprite); // Use stored sprite reference
        this.effects.createSpiralParticles(this.effectsContainer, {
          x: paddle.x,
          y: paddle.y
        });
      });
    }
  }

  upgradeBallSpeed() {
    if (this.score >= this.ballSpeedCost) {
      this.score -= this.ballSpeedCost;
      this.ballSpeed *= 1.2;
      this.ballSpeedCost *= 2;
      
      // Upgrade effects
      this.balls.children.forEach(ball => {
        this.effects.highlightCharacter(ball.sprite); // Use stored sprite reference
        this.effects.createSpiralParticles(this.effectsContainer, {
          x: ball.x,
          y: ball.y
        });
      });
    }
  }

  upgradeMultiBall() {
    if (this.score >= this.multiBallCost) {
      this.score -= this.multiBallCost;
      this.ballCount++;
      this.createBall();
      this.multiBallCost *= 2;
      this.effects.screenShake(this.app.stage, { intensity: 8 });
    }
  }

  upgradePointsMultiplier() {
    if (this.score >= this.pointsMultiplierCost) {
      this.score -= this.pointsMultiplierCost;
      this.pointsMultiplier *= 2;
      this.pointsMultiplierCost *= 2;
      
      // Upgrade effects
      this.effects.screenShake(this.app.stage, { intensity: 8 });
      [this.leftPaddle, this.rightPaddle, ...this.balls.children].forEach(obj => {
        this.effects.createSpiralParticles(this.effectsContainer, {
          x: obj.x,
          y: obj.y
        });
      });
    }
  }

  upgradePaddleSpeed() {
    if (this.score >= this.paddleSpeedCost) {
      this.score -= this.paddleSpeedCost;
      this.paddleSpeed *= 1.2;
      this.paddleSpeedCost *= 2;
      
      // Upgrade effects
      [this.leftPaddle, this.rightPaddle].forEach(paddle => {
        this.effects.highlightCharacter(paddle.sprite); // Use stored sprite reference
        this.effects.createSpiralParticles(this.effectsContainer, {
          x: paddle.x,
          y: paddle.y
        });
      });
    }
  }

  destroy() {
    this.effects.destroyAll();
    this.app.destroy(true);
  }
}
