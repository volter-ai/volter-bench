# Overview
Title: coffee_tycoon_3

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn money (primary currency) when customers receive their coffee and pay at the register. Each coffee sale generates a fixed amount of money.

## Core Game
Customers automatically spawn at the entrance of the coffee shop. Baristas work at coffee stations making coffee. When a coffee is ready, the barista brings it to the counter. Customers walk to the counter, pick up their coffee, pay at the register, and leave through the exit. New customers continue to arrive as long as there is space in the shop.

## Movement System
- Customers move in a straight line from entrance → counter → register → exit
- Baristas move between coffee station and counter to deliver completed drinks
- All movement is simple point-to-point without pathfinding
- Entities move at constant speeds in straight lines

## Upgrades
- Number of baristas (more workers = more coffee production)
- Coffee making speed (baristas make coffee faster)
- Customer capacity (more customers can be in shop at once)
- Coffee price (each sale generates more money)
- Barista efficiency (baristas can carry multiple coffees)
