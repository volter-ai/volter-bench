# Overview
Title: pong_1

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Player earns points whenever the ball hits either paddle. The number of points earned per hit can be upgraded.

## Core Game
Two AI-controlled paddles play an endless game of pong. The ball bounces between the paddles automatically. The paddles will attempt to hit the ball but may occasionally miss. When a paddle misses, the ball resets to the center and continues play. Score accumulates with each successful paddle hit.

## Movement System
- Paddles move up and down automatically to track the ball's vertical position
- Ball moves in straight lines at constant speed
- Ball bounces off paddles and top/bottom walls at simple angles
- When ball goes past a paddle, it resets to center with a random direction

## Upgrades
- Paddle Size: Increases the height of both paddles
- Ball Speed: Increases how fast the ball moves
- Points Per Hit: Increases how many points are earned when the ball hits a paddle
- Paddle Speed: How quickly the paddles can move to track the ball
- Paddle Accuracy: Improves how well the paddles predict where the ball will be
