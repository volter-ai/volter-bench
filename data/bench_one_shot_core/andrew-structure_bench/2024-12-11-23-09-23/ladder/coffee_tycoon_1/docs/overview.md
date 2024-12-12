# Overview
Title: coffee_tycoon_1

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn money (primary currency) when baristas serve coffee to customers. Each customer pays a fixed amount when served their coffee.

## Core Game
Customers automatically appear at a counter on the left side of the screen. Baristas move to the coffee machine to prepare coffee, then serve it to waiting customers. Each customer has a coffee order displayed above them.

There is a coffee machine in the middle of the screen where baristas prepare drinks. The right side has a serving counter where completed orders are delivered to customers.

New customers appear automatically when previous customers are served. Multiple customers can wait in line.

## Movement System
Baristas move in straight lines between three points:
1. Coffee machine (center) to make coffee
2. Serving counter (right) to deliver coffee
3. Return to starting position to serve next customer

No diagonal movement or complex pathfinding needed. Baristas move directly between points.

## Upgrades
- Number of baristas (serve more customers simultaneously)
- Barista movement speed (faster coffee delivery)
- Coffee machine efficiency (faster coffee preparation)
- Customer capacity (more customers can wait in line)
- Coffee price (more money per customer)
