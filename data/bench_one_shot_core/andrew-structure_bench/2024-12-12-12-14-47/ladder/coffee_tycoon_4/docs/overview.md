# Overview
Title: coffee_tycoon_4

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn money ($) when customers pick up their completed coffee orders. Each basic coffee order generates $5. Customers automatically appear, order, and leave with their drinks.

## Core Game
Customers automatically spawn at the entrance and walk to the counter. Baristas take their orders and move to the coffee station to prepare drinks. When drinks are ready, baristas place them at the pickup counter. Customers collect their drinks and leave, generating money.

New customers appear at a steady rate as long as there is space in the shop. Each customer's order status is displayed above them.

## Movement System
Entities move in straight lines between key points:
- Customers: Entrance → Counter → Pickup Area → Exit
- Baristas: Counter → Coffee Station → Pickup Counter → Back to Counter

All movement is automatic and follows these fixed paths. No diagonal movement or complex pathfinding required.

## Upgrades
- Additional Baristas ($100 base): Increases order processing capacity
- Barista Speed ($150 base): Makes baristas move and work faster
- Customer Capacity ($200 base): Allows more customers in the shop simultaneously
- Coffee Price ($250 base): Increases money earned per order
- Order Processing Speed ($300 base): Reduces time to make coffee
