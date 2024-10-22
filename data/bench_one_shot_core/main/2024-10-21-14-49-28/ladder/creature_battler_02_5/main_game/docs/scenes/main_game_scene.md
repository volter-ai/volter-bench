# MainGameScene

The Main Game Scene is where the human player does battle against a bot player using their teams of creatures. This is a scene that can be played by one player, but should be treated like a symmetric multiplayer scene.

## Scene Logic

The scene plays through repeating turns with distinct phases. Turns consist of:
- Player Choice Phase
- Foe Choice Phase
- Resolution Phase

### Player Choice Phase

During the player choice phase, the player is shown their creature's list of available skills. The player is able to choose one of those skills and that is queued for the resolution phase.

### Foe Choice Phase

During the foe choice phase, the opposing player is shown their own creature's list of available skills and chooses one from that list. This skill is also queued for the resolution phase.

### Resolution Phase

During the resolution phase, the skills that were queued in the previous two steps are resolved. 

The order in which the skills are executed depends on the speed of the creature using the skill. The creature that has the higher speed stat executes their skill first. If the creatures have the same speed, then which creature goes first is decided randomly, with either creature having equal chance of being picked to go first.

#### Skill Execution

When executing a skill, the damage dealt is calculated as the skill's base damage plus the attacker's attack minus the defender's defense. In other words:
```
[damage] = [attacker attack] + [skill base damage] - [defender defense]
```
The calculated damage value is subtracted from the defender's hp. 

### Battle End Condition

At any point when one creature's hp reaches zero, the battle ends. At that point, a message is shown informing the player whether they have won or lost depending on which creature was knocked out.
- If the player's creature was defeated, then they are informed that they are the loser.
- If the opponent's creature's hp is reduced to zero, then the player is informed that they are the winner.