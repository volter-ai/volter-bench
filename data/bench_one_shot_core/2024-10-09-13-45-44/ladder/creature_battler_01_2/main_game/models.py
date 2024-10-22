from __future__ import annotations

from typing import List

from mini_game_engine.engine.lib import AbstractPlayer, AbstractThing


class Skill(AbstractThing):
    damage: int
    description: str

class Creature(AbstractThing):
    hp: int
    max_hp: int
    skills: List[Skill]

class Player(AbstractPlayer):
    creatures: List[Creature]
