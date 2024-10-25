from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self._foe_choice_phase()
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            if self._check_battle_end():
                break

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, foe_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent_creature, self.player_creature, foe_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent_creature, self.player_creature, foe_skill)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
        else:
            # Equal speed, random order
            if random.choice([True, False]):
                self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
                if self.opponent_creature.hp > 0:
                    self._execute_skill(self.opponent_creature, self.player_creature, foe_skill)
            else:
                self._execute_skill(self.opponent_creature, self.player_creature, foe_skill)
                if self.player_creature.hp > 0:
                    self._execute_skill(self.player_creature, self.opponent_creature, player_skill)

    def _execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! It dealt {final_damage} damage.")

    def _calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}, you have lost the battle!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"Congratulations {self.player.display_name}, you have won the battle!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
