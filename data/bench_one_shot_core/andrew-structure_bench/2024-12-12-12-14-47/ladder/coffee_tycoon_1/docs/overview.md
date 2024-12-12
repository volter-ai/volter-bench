# Overview
Title: coffee_tycoon_1

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn money (primary currency) when customers receive their coffee and pay before leaving the shop. Each coffee sale generates a base amount of $5.

## Core Game
Customers automatically spawn at the shop entrance. Baristas work at coffee machines to prepare drinks. When a drink is ready, baristas carry it to waiting customers. After receiving their coffee, customers pay and exit the shop.

The coffee machines show a progress bar while preparing drinks. Customers have a small indicator showing they are waiting for coffee.

New customers appear when there is available space in the shop and existing customers leave.

## Movement System
- Customers move in a straight line from entrance to waiting area
- Baristas move between coffee machines and customers in straight lines
- Customers exit through the entrance after being served
- All movement is instant with no animations, just position updates

## Upgrades
- Additional Baristas ($50 base cost)
- Barista Movement Speed ($30 base cost)
- Coffee Machine Brewing Speed ($40 base cost)
- Maximum Customers in Shop ($60 base cost)
- Coffee Price Multiplier ($100 base cost)
