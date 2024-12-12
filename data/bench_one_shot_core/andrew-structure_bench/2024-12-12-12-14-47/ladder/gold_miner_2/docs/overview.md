# Overview
Title: gold_miner_2

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn gold when miners deposit their cargo at the central depot. Each miner automatically travels to mines, collects gold, and returns to deposit it. The amount of gold earned per deposit depends on the miner's carrying capacity.

## Core Game
Multiple gold mines appear on the screen, each containing a finite amount of gold. Automated miners travel between the mines and a central depot. When a miner reaches a mine, they collect gold up to their carrying capacity. They then return to the depot to deposit the gold, which adds to the player's currency. When a mine is depleted, it disappears and a new one spawns in a random location.

## Movement System
Miners move in straight lines between their current position and their destination (either a mine or the depot). When a miner needs to collect gold, they target the nearest non-empty mine. After collecting, they move directly to the depot. Once they've deposited their gold, they select a new mine and repeat the cycle.

## Upgrades
- Miner Count: Add additional miners to collect gold simultaneously
- Mining Speed: Increase the movement speed of all miners
- Carrying Capacity: Increase how much gold each miner can carry per trip
- Maximum Mines: Increase the number of mines that can exist simultaneously
- Mine Size: Increase the amount of gold in each mine
