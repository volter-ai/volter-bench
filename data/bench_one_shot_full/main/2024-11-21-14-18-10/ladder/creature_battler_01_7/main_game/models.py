from __future__ import annotations
from typing import List
from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing, Collection

class Skill(AbstractThing):
    category: str = "Skill"
    damage: int

class Creature(AbstractThing):
    category: str = "Creature" 
    hp: int
    max_hp: int
    skills: List[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: List[Creature]

    def reset_creatures(self):
        """Reset creatures to their original state"""
        for creature in self.creatures:
            creature.hp = creature.max_hp
