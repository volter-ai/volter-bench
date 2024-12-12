# Overview
Title: infinite_runner_3

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn coins when runners collect them from the tracks. Coins appear automatically on the tracks at regular intervals. When a runner touches a coin, it's collected and added to the player's total.

## Core Game
Multiple parallel tracks extend from left to right. AI-controlled runners automatically run forward on these tracks. Coins spawn randomly on the tracks. Obstacles occasionally appear that runners must avoid by switching tracks. Each runner automatically collects coins they touch while avoiding obstacles. New runners start from the left side when they reach the right edge of the screen.

## Movement System
- Runners move continuously from left to right at a constant speed
- When encountering an obstacle, runners move one track up or down to avoid it
- When reaching the right edge, runners instantly return to the left side
- Runners automatically pick the track with the most coins when choosing where to move

## Upgrades
- Number of simultaneous runners
- Runner movement speed
- Coin value multiplier
- Coin spawn frequency
- Number of parallel tracks
- Runner collision radius (makes it easier to collect coins)
