# MainGameScene

The Main Game Scene is where the human player does battle against a bot player using their teams of creatures. This is a scene that can be played by one player, but should be treated like a symmetric multiplayer scene.

## Scene Logic

The scene starts off by putting the player's first creature out as the active creature participating in battle.

The scene plays through repeating turns with distinct phases. Turns consist of:
- Player Choice Phase
- Foe Choice Phase
- Resolution Phase

### Player Choice Phase

The player choice phase is a branching series of choices. It begins by offering the player two choices, which then leads to a new set of choices to get shown to the player.
- "Attack" - The player's active creature's skills are shown as choices. When the player chooses one of these skills, it is added to the queue of the actions for the turn and the turn proceeds to the next phase. The player also is shown the choice to go "Back", which sends the player back to the previous set of choices.
- "Swap" - The player's list of creatures are shown as a list of choices. The player's active creature and any creatures with zero hp are excluded from this list. When the player chooses one of the creatures, it is added to the queue of actions for the turn and the turn proceeds to the next phase. The player also is shown the choice to go "Back", which sends the player back to the previous set of choices.

### Foe Choice Phase

The foe choice phase is identical to the player choice phase, but instead is played by the bot player instead of the human player.

### Resolution Phase

During the resolution phase, the actions that were queued in the previous two steps are resolved. 

The order in which the skills are executed depends on the speed of the creature using the skill. The creature that has the higher speed stat executes their skill first. If the creatures have the same speed, then which creature goes first is decided randomly, with either creature having equal chance of being picked to go first.

However, if either player chooses to swap creatures, that is always executed before skills. The creature that gets swapped in gets hit by its opponent's queued skill.

#### Skill Execution

When executing a skill, the damage dealt is calculated in two passes. First, a raw damage value is calculated in one of two ways depending on whether the skill is physical or if it is a non-physical (special) skill.

If the skill is physical, then the raw damage is calculated as the skill's base damage plus the attacker's attack minus the defender's defense. In other words:
```
[raw damage] = [attacker attack] + [skill base damage] - [defender defense]
```

If the skill is non-physical (special), then the raw damage is calculated as the ratio between the attacker's sp. attack and the defender's sp. defense multiplied against the skill's base damage:
```
[raw damage] = [attacker sp. attack]/[defender sp. defense] * [skill base damage]
```

The final damage is then calculated by taking the raw damage and multiplying it by a weakness-resistance factor depending on the matchup of the skill type against the defender's creature type:
```
[final damage] = [weakness-resistance factor] * [raw damage]
```
All the damage formulas should be performed with floats, and then converted to an integer as the final damage. The final damage value is subtracted from the defender's hp. 

#### Type Relationships

When calculating the damage dealt by a skill, a weakness-resistance factor needs to be found by comparing the skill type against the defender's creature type. 
- If a skill type is effective against a creature type, the factor is 2 (the skill does double damage). 
- If a skill type is ineffective  against a creature type, the factor is 1/2 (the skill does half damage).

The following are the relationships between the handful of types in the game:
- "Normal" | Is neither effective nor ineffective against any other types.
- "Fire" | Effective against Leaf | Ineffective against Water
- "Water" | Effective against Fire | Ineffective against Leaf
- "Leaf" | Effective against Water | Ineffective against Fire

### Forced Swapping & Battle End

At any point when one creature's hp reaches zero (it is considered "knocked-out"), the creature's owner (a player) is asked to swap to another creature as long as they have any creatures with nonzero hp. This is presented as a list of choices of those creatures. If a player has no creatures available, then the battle ends. The player with all of their creatures knocked out is considered the loser and the other player is the winner. The player is then informed of their win or loss, depending on whether they still have creatures with nonzero hp.

When leaving this scene, reset the state of the player's creatures.