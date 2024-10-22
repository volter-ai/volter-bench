import random

from main_game.models import Creature, Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        battle_ended = False
        while not battle_ended:
            # Player turn
            player_skill = self._player_turn()
            
            # Opponent turn
            opponent_skill = self._opponent_turn()
            
            # Resolve turn
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            battle_ended = self._check_battle_end()

        # Transition back to the main menu after the battle ends
        self._transition_to_scene("MainMenuScene")

    def _player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
        else:
            # Equal speed, randomly decide who goes first
            if random.choice([True, False]):
                self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
                if self.opponent_creature.hp > 0:
                    self._execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
            else:
                self._execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
                if self.player_creature.hp > 0:
                    self._execute_skill(self.player_creature, self.opponent_creature, player_skill)

    def _execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_factor = self._get_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)
        
        effectiveness = "It's super effective!" if weakness_factor > 1 else "It's not very effective..." if weakness_factor < 1 else ""
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{effectiveness}")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def _get_weakness_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0  # Normal type is neither effective nor ineffective against any type
        elif defender_type == "normal":
            return 1.0  # All types are normally effective against Normal type
        elif skill_type == defender_type:
            return 1.0
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2.0
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0.5
        else:
            return 1.0

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
