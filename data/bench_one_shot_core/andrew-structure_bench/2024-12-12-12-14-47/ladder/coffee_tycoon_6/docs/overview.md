# Overview
Title: coffee_tycoon_6

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn money ($) when customers pick up their completed coffee orders. Each basic coffee order generates $5. Customers automatically spawn, order, and collect their drinks without player intervention.

## Core Game
Customers automatically enter the coffee shop from the left side. They move to the counter where a barista takes their order. The barista then moves to the coffee station to prepare the drink. Once ready, the drink is placed at the pickup counter where the customer collects it and leaves, generating money.

New customers spawn at a steady rate as long as there is space in the shop. Each customer follows the same pattern:
1. Enter shop
2. Order at counter
3. Wait at pickup area
4. Collect drink and leave

## Movement System
- Customers move in straight lines:
  * From entrance to counter
  * From counter to pickup area
  * From pickup area to exit
- Baristas move in straight lines:
  * Between counter and coffee station
  * Between coffee station and pickup counter

All movement is instant with no animations, just position updates to show current status.

## Upgrades
1. Additional Baristas ($50 base) - Increases number of orders that can be processed simultaneously
2. Barista Speed ($30 base) - Reduces time needed to make coffee
3. Coffee Machine Efficiency ($40 base) - Reduces coffee preparation time
4. Customer Capacity ($25 base) - Increases maximum number of customers allowed in shop
5. Coffee Price ($60 base) - Increases money earned per order
