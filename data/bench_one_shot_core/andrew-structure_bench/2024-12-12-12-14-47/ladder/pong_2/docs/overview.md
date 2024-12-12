# Overview
Title: pong_2

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Player earns points whenever either paddle successfully hits the ball. Points are the primary currency.
Additional points are earned based on the current ball speed - faster balls generate more points per hit.

## Core Game
Two AI-controlled paddles play an endless game of pong. The ball moves between them, gradually speeding up.
When a paddle misses the ball, the game resets to base speed.
The longer the volley continues, the more points are earned per hit due to increased ball speed.
Score/points display at the top of the screen.

## Movement System
- Paddles move up and down automatically to track the ball's vertical position
- Ball moves in straight lines, bouncing off paddles and top/bottom walls
- When ball hits a paddle, it reflects at a slight random angle
- Ball speed increases by a small amount after each successful paddle hit
- All movement is linear with no acceleration or complex physics

## Upgrades
1. Paddle Height: Increases the size of both paddles, making it easier to hit the ball
2. Paddle Speed: Makes paddles move faster to reach the ball
3. Point Multiplier: Increases points earned per successful hit
4. Starting Ball Speed: Increases the base speed when game resets
5. Speed Scaling: Increases how much the ball speeds up after each hit
