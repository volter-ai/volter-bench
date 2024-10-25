# Overview

This is the overview document for a creature battler game. In this game, the player assembles a team of creatures to fight against another player's team of creatures to see who can reduce their opponent's health to zero first.

## Game Scenes

- **MainMenuScene** - This is the starting scene and where the player can choose to play or quit.
- **MainGameScene** - This is the scene where the action takes place. Here, the player does battle against a bot opponent.

## Game Entities

- **Player** - A thing that represents a human or bot within the game, and is controlled by the human or bot.
- **Creature** - A thing that does battle within the game. **Player**s handle a team of creatures in battle.
- **Skill** - A thing that represents the actions that the **Creature**s are able to take in battle.