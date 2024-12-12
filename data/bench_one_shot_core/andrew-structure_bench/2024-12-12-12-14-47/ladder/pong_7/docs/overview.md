# Overview
Title: pong_7

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Player earns points whenever the ball hits either paddle. Points are the primary currency used to purchase upgrades.

## Core Game
Two AI-controlled paddles play an endless game of pong. The paddles automatically track and move to intercept balls. Multiple balls can be in play simultaneously. Each ball gradually speeds up until a point is scored, then resets to base speed. The game continues indefinitely, generating points with each paddle hit.

## Movement System
- Paddles move up and down vertically along the left and right edges
- Each paddle automatically moves toward the y-position of the nearest ball
- Balls move in straight lines, bouncing off paddles and top/bottom walls
- When a ball scores (passes a paddle), it resets to the center with a random direction

## Upgrades
- Paddle Size: Increases height of both paddles
- Ball Speed: Increases base movement speed of all balls
- Multi-Ball: Adds additional balls to the game
- Points Per Hit: Multiplies points earned when balls hit paddles
- Paddle Speed: Increases how quickly paddles can move to catch balls
