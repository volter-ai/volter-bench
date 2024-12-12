# Overview
Title: coffee_tycoon_7

## Genre
Auto-playing idle/incremental game. The entire game except for the upgrades is fully automated. The player will earn more of the primary currency over time

The cost of each upgrade doubles with each purchase.

## Currency Accumulation
Players earn money (primary currency) when customers purchase coffee. Each coffee sale generates a base amount of $5. Customers automatically appear, order coffee, receive their drink from baristas, pay, and leave.

## Core Game
The game takes place in an automated coffee shop. Customers regularly appear at the entrance and line up at the counter. Baristas work between the counter and coffee machines, preparing drinks for customers. When a barista serves a completed drink to a customer, money is earned.

New customers appear at a steady rate as long as there is space in the shop. Each coffee machine can only be used by one barista at a time. Customers leave after being served or if they wait too long.

The shop displays:
- Current money
- Number of customers waiting
- Number of drinks being prepared
- Number of available coffee machines

## Movement System
Entities move in straight lines between fixed points:

Customers:
- Move from entrance to counter
- Wait at counter
- Move from counter to exit after being served

Baristas:
- Move from counter to coffee machine
- Wait at machine while preparing coffee
- Move back to counter to serve customer

## Upgrades
- Additional Baristas ($100 base) - More workers to make coffee
- Additional Coffee Machines ($200 base) - More stations to prepare drinks
- Faster Baristas ($150 base) - Reduces coffee preparation time
- Larger Shop Space ($300 base) - Allows more customers to wait in line
- Better Coffee Quality ($250 base) - Increases money earned per sale
