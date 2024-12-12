# Overview
Title: tank_attack_6

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Player earns credits when their tanks destroy enemy tanks. Each destroyed enemy tank awards a fixed amount of credits.

## Core Game
Friendly tanks and enemy tanks exist on a 2D battlefield. Enemy tanks spawn randomly at the edges of the screen. Friendly tanks automatically target and shoot at the nearest enemy tank. When an enemy tank is destroyed, credits are awarded and a new enemy tank spawns after a short delay.

Each tank has a health bar displayed above it. When a tank's health reaches zero, it is destroyed.

## Movement System
- Friendly tanks move directly toward their target enemy tank
- Enemy tanks move in straight lines toward the center of the screen
- When tanks are in range of their target, they stop moving and start shooting
- Tanks rotate to face their target
- All movement is at constant speed without acceleration

## Upgrades
- Tank Count: Add additional friendly tanks
- Tank Speed: Increase movement speed of friendly tanks
- Tank Damage: Increase damage per shot
- Tank Health: Increase health points of friendly tanks
- Fire Rate: Decrease time between shots
- Range: Increase shooting distance
