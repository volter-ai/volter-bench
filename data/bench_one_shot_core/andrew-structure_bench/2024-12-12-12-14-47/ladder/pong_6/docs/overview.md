# Overview
Title: pong_6

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Player earns points whenever either paddle successfully hits the ball. Points are the primary currency.
Each successful hit adds to the point total.
Consecutive hits without missing increase the point multiplier temporarily.

## Core Game
Two AI-controlled paddles play an endless game of pong against each other.
The ball bounces between the paddles, gradually increasing in speed.
When a paddle misses the ball, the game resets with base speed.
The goal is to accumulate points through successful paddle hits.
A score multiplier increases with consecutive hits.

## Movement System
- Paddles move up and down automatically to track the ball's vertical position
- Ball moves in straight lines, bouncing off paddles and top/bottom walls
- When ball hits a paddle, it reflects at a slight random angle
- Ball speed increases gradually until a paddle misses
- After a miss, ball resets to center with base speed

## Upgrades
1. Paddle Height: Increases the size of both paddles
2. Paddle Speed: Makes paddles move faster to track the ball
3. Point Multiplier: Increases base points earned per hit
4. Starting Ball Speed: Increases the initial speed of the ball
5. Paddle Prediction: Improves AI paddle accuracy
6. Combo Multiplier: Increases points earned from consecutive hits
