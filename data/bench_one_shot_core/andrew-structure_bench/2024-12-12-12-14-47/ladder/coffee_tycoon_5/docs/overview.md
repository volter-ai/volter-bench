# Overview
Title: coffee_tycoon_5

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn money ($) when baristas complete coffee orders for customers. Each customer pays a fixed amount when their order is fulfilled and they receive their coffee.

## Core Game
Customers automatically appear at ordering counters. AI-controlled baristas move between coffee machines and counters to prepare and serve drinks. Each counter shows a customer waiting with their order. When a barista delivers the coffee, money is earned and the customer leaves, making room for a new customer.

Multiple service counters and coffee machines exist in the shop. Baristas automatically choose the nearest available customer and coffee machine to optimize service.

## Movement System
Baristas move in straight lines between three points:
1. Counter (to take order)
2. Coffee machine (to prepare drink)
3. Back to counter (to serve drink)

Customers appear at counters and disappear when served. No complex pathfinding needed.

## Upgrades
- Number of Baristas: Increases parallel order processing
- Barista Speed: Makes baristas move faster between stations
- Coffee Machine Efficiency: Reduces time to make drinks
- Additional Service Counters: Allows more simultaneous customers
- Coffee Price: Increases money earned per order
- Customer Attraction: Reduces time between customer appearances
