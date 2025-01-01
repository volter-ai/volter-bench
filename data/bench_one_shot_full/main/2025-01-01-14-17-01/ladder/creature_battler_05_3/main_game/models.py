from __future__ import annotations
from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing, create_from_game_database
from typing import List

class Skill(AbstractThing):
    category: str = "Skill"
    skill_type: str
    is_physical: bool
    base_damage: int

class Creature(AbstractThing):
    category: str = "Creature"
    creature_type: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    skills: List[Skill]

class Player(AbstractPlayer):
    category: str = "Player"
    creatures: List[Creature]
    active_creature: Creature

    def __init__(self, **data):
        super().__init__(**data)
        if self.creatures:
            self.active_creature = self.creatures[0]
