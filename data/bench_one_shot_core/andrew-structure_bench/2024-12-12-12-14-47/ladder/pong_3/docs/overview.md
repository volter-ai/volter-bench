# Overview
Title: pong_3

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Player earns points whenever the ball hits either paddle. Points are the primary currency used to purchase upgrades.

## Core Game
Two AI-controlled paddles play an endless game of pong. The paddles automatically move to intercept the ball. When the ball hits a paddle, points are earned. If the ball goes past a paddle, it respawns in the center. Multiple balls can be in play simultaneously based on upgrades.

## Movement System
- Paddles move up and down automatically to track the nearest ball
- Balls move in straight lines, bouncing off paddles and top/bottom walls
- When a ball goes past a paddle, it respawns in the center with a random direction
- All movement is linear with constant speeds (modified by upgrades)

## Upgrades
- Ball Speed: Increases how fast balls move
- Paddle Size: Makes paddles taller
- Multi-Ball: Adds additional balls to the game
- Paddle Speed: Makes paddles move faster
- Points Per Hit: Multiplies points earned when ball hits paddle
