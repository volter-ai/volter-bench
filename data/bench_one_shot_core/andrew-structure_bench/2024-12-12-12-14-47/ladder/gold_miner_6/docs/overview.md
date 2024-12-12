# Overview
Title: gold_miner_6

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn Space Crystals when drones deposit their cargo at the central space station. Each deposit adds to the total crystal count based on the drone's carrying capacity.

## Core Game
Automated drones fly between randomly spawning asteroids and a central space station. Each asteroid contains a finite amount of Space Crystals, displayed as a progress bar above it. When an asteroid is depleted, it disappears and a new one spawns at a random location on the screen.

The space station remains fixed in the center of the screen. Multiple drones can mine different asteroids simultaneously. Each drone will select the nearest available asteroid to mine.

## Movement System
Drones move in straight lines between their current position and their target (either asteroid or space station). When a drone reaches an asteroid, it stays there briefly to "mine" before returning to the station. After depositing at the station, it immediately seeks the next closest asteroid.

## Upgrades
1. Drone Count: Add additional drones to collect crystals (starts with 1)
2. Mining Speed: Reduce the time needed to extract crystals from asteroids
3. Cargo Capacity: Increase how many crystals each drone can carry per trip
4. Drone Speed: Increase movement speed of all drones
5. Asteroid Richness: Increase the amount of crystals contained in each asteroid
6. Maximum Asteroids: Increase the number of asteroids that can exist simultaneously
