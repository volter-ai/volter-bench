# Overview
Title: pong_5

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Player earns points whenever the ball successfully hits either paddle. This creates a steady stream of points as the AI paddles keep the ball(s) in play.

## Core Game
Two AI-controlled paddles play an endless game of pong. The paddles automatically move to intercept the ball(s). When a ball hits a paddle, the player earns points. If a ball goes past a paddle, it respawns in the center with a random direction.

Multiple balls can be in play simultaneously based on upgrades. Each ball bounces off the top and bottom walls and the paddles.

## Movement System
- Paddles move up and down tracking their assigned ball
- Balls move in straight lines at constant speed
- Balls bounce off walls and paddles at appropriate angles
- When a ball is missed, it respawns in the center moving in a random direction

## Upgrades
1. Ball Speed - Increases how fast the balls move
2. Paddle Size - Makes the paddles taller
3. Multi-ball - Adds additional balls to the game
4. Paddle Speed - Makes the paddles move faster
5. Points Per Hit - Increases points earned when ball hits paddle
