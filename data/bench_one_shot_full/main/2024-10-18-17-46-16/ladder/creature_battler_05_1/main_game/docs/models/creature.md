# Creature

Creature is an entity in the creature battler game that participates in battles.

## Additional Attributes

- `creature_type` - A string representing the creature's elemental affinity. This decides the creature's weaknesses and resistances.
- `hp` - An integer representing the number of health points the creature has. The creature is knocked out when this number reaches zero.
- `max_hp` - An integer representing the maximum number of health points a creature can have.
- `attack` - An integer representing the added power behind the creature's physical attacks.
- `defense` - An integer representing the creature's physical resistance to physical attacks.
- `sp_attack` - An integer representing the added power behind the creature's non-physical attacks.
- `sp_defense` - An integer representing the creature's physical resistance to non-physical attacks.
- `speed` - An integer representing the creature's priority when deciding turn order.
- `skills` - A collection of the skills that the creature has access to in battle.