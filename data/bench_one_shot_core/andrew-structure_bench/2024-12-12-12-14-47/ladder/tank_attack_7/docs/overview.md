# Overview
Title: tank_attack_7

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Player earns credits when their tanks destroy enemy tanks. Each destroyed enemy tank awards a fixed amount of credits.

## Core Game
Friendly tanks automatically patrol a battlefield. Enemy tanks spawn randomly at the edges of the screen. When a friendly tank detects an enemy tank, it moves toward it and fires. Each successful hit damages the enemy tank. When an enemy tank is destroyed, credits are awarded and a new enemy tank spawns after a short delay.

The game displays the current credit count prominently at the top of the screen. Enemy tanks have visible health bars above them.

## Movement System
Tanks move in straight lines toward their targets. When no enemies are present, friendly tanks move in a simple patrol pattern between random points on their half of the screen. Enemy tanks move in straight lines toward the nearest friendly tank.

Tanks rotate instantly to face their target direction - no turning animations needed. This keeps the movement system clear and functional.

## Upgrades
- Tank Count: Add additional friendly tanks to the battlefield
- Tank Speed: Increase movement speed of friendly tanks
- Tank Damage: Increase damage dealt per shot
- Tank Health: Increase durability of friendly tanks
- Fire Rate: Reduce time between shots
- Detection Range: Increase the range at which friendly tanks can spot enemies
