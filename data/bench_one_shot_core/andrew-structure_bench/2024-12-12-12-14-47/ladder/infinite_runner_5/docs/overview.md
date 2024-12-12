# Overview
Title: infinite_runner_5

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn coins when runners collect coin pickups that randomly spawn on the tracks. Each coin pickup adds to the total coin count.

## Core Game
Multiple parallel horizontal tracks contain runners that automatically move from right to left. Coin pickups randomly spawn on the tracks. When runners collide with coins, they collect them and add to the player's total. When runners reach the left edge, they teleport back to the right side to continue running. New coins spawn at regular intervals.

## Movement System
Runners move at a constant speed from right to left along their assigned tracks. When reaching the left edge, runners instantly teleport to the right edge of their track. Coins remain stationary until collected. No complex animations, just simple position updates.

## Upgrades
- Number of active runners (more runners = more coin collection opportunities)
- Runner speed (faster runners cover more ground and collect more coins)
- Coin value (each collected coin is worth more)
- Coin spawn rate (more coins appear on tracks)
- Multi-track unlock (enables additional parallel tracks for more runners)
