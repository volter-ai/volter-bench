# Game Balance Analysis

## Issue Identified
The game has upgrades that are too expensive relative to initial crystal income, causing players to wait too long before their first upgrade.

## Evidence from Logs
1. First crystal delivery occurs at ~14 seconds (10 crystals)
2. Cheapest upgrades cost 15 crystals
3. Players must wait for second delivery to afford first upgrade
4. First upgrade occurs at ~28 seconds (too long)

## Solution Implemented
1. Reduced cost of MINING_SPEED upgrade from 15 to 10 crystals
2. Reduced cost of DRONE_SPEED upgrade from 15 to 10 crystals
3. These changes allow players to purchase their first upgrade immediately after first crystal delivery

## Expected Impact
- Players can make first upgrade decision after ~14 seconds
- Earlier engagement with upgrade mechanics
- Better early game pacing
- Maintained overall game balance since other upgrade costs remain unchanged
