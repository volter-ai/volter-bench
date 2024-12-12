# Overview
Title: tank_attack_1

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Player earns coins when tanks destroy enemy bases. Each destroyed base awards a fixed amount of coins.

## Core Game
Friendly tanks automatically spawn on the left side of the screen. Enemy bases appear on the right side. Tanks move towards the bases and automatically fire when in range. When a base is destroyed, the player receives coins and a new base spawns after a short delay.

Multiple tanks can attack the same base. Each base has a health bar displayed above it. The number of coins earned is displayed when a base is destroyed.

## Movement System
- Tanks move in a straight line from left to right
- When a tank reaches firing range of a base, it stops moving
- When a base is destroyed, tanks will move toward the next available base
- New tanks spawn at regular intervals on the left side at random y-positions
- New bases spawn on the right side at random y-positions when previous bases are destroyed

## Upgrades
- Tank Damage: Increases damage dealt by tanks
- Tank Speed: Makes tanks move faster
- Tank Fire Rate: Reduces time between shots
- Max Tanks: Increases the maximum number of tanks that can exist simultaneously
- Multi-shot: Allows tanks to hit multiple bases with each shot
- Base Coin Value: Increases coins earned per destroyed base
