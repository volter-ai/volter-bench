import math
import random

from main_game.models import Creature, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
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
        self._show_text(self.player, "Battle start!")
        battle_ended = False
        while not battle_ended:
            battle_ended = self._battle_round()
        self._reset_creatures()
        self._return_to_main_menu()

    def _battle_round(self):
        player_skill = self._player_choice_phase()
        opponent_skill = self._opponent_choice_phase()
        return self._resolution_phase(player_skill, opponent_skill)

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _opponent_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, opponent_skill):
        first, second = self._determine_order()
        for attacker, defender, skill in [(first, second, player_skill if first == self.player else opponent_skill),
                                          (second, first, opponent_skill if first == self.player else player_skill)]:
            damage = self._calculate_damage(attacker.creatures[0], defender.creatures[0], skill)
            defender.creatures[0].hp = max(0, defender.creatures[0].hp - damage)
            self._show_text(self.player, f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name}!")
            self._show_text(self.player, f"{defender.display_name}'s {defender.creatures[0].display_name} took {damage} damage!")
            
            if defender.creatures[0].hp == 0:
                self._show_text(self.player, f"{defender.display_name}'s {defender.creatures[0].display_name} fainted!")
                self._show_text(self.player, f"{attacker.display_name} wins!")
                return True
        return False

    def _determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.opponent
        elif self.player_creature.speed < self.opponent_creature.speed:
            return self.opponent, self.player
        else:
            return random.sample([self.player, self.opponent], 2)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        return math.floor(raw_damage * type_factor)

    def _get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1  # Normal type is neither effective nor ineffective
        
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def _return_to_main_menu(self):
        self._show_text(self.player, "Returning to main menu...")
        self._transition_to_scene("MainMenuScene")
