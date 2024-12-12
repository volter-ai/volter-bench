# Overview
Title: pong_4

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Player earns points whenever the ball successfully hits either paddle. This creates a steady stream of points as the AI paddles keep the ball in play.

## Core Game
Two AI-controlled paddles play an endless game of pong. The paddles automatically move to intercept the ball, keeping it in play as much as possible. The ball bounces between the paddles, generating points on each successful hit. If the ball is missed, it immediately respawns in the center with a random direction.

## Movement System
- Paddles move up and down vertically to track the ball's position
- Ball moves in straight lines, bouncing off paddles and top/bottom walls
- When ball hits a paddle, it reflects at a slight random angle
- Ball speed is constant until modified by upgrades
- Paddles move at a constant speed until modified by upgrades

## Upgrades
- Ball Speed: Increases how fast the ball moves, leading to more frequent paddle hits
- Paddle Size: Makes paddles taller, reducing chances of missing the ball
- Paddle Speed: Makes paddles move faster, improving their ability to catch the ball
- Point Multiplier: Increases points earned per paddle hit
- Multi-ball: Adds additional balls to the game (up to a maximum)
