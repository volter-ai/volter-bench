# Overview
Title: infinite_runner_4

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn coins when runners collect them from the tracks. Coins appear automatically on the tracks at regular intervals. When a runner touches a coin, it's collected and added to the player's total.

## Core Game
Multiple parallel tracks extend from left to right. AI-controlled runners automatically move forward along these tracks. Coins spawn randomly on the tracks. Obstacles occasionally appear that runners must avoid by switching tracks. Each runner automatically collects coins they touch while avoiding obstacles. New runners start from the left side when previous runners reach the right side.

## Movement System
- Runners move automatically from left to right at a constant speed
- When approaching an obstacle, runners move one track up or down to avoid it
- When a runner reaches the right side, they teleport back to the left side
- Runners prioritize tracks with coins when choosing where to move

## Upgrades
- Number of simultaneous runners
- Runner movement speed
- Coin spawn frequency
- Coin value multiplier
- Number of parallel tracks
- Runner coin collection radius
