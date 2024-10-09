from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot_player = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot_player.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Bot's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Bot Choice Phase
            bot_skill = self._player_choice_phase(self.bot_player, self.bot_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, bot_skill)
            
            if self._check_battle_end():
                self._transition_to_scene("MainMenuScene")
                break

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill: Skill, bot_skill: Skill):
        if self.player_creature.speed > self.bot_creature.speed:
            self._execute_skill(self.player, self.player_creature, player_skill, self.bot_player, self.bot_creature)
            if self.bot_creature.hp > 0:
                self._execute_skill(self.bot_player, self.bot_creature, bot_skill, self.player, self.player_creature)
        elif self.player_creature.speed < self.bot_creature.speed:
            self._execute_skill(self.bot_player, self.bot_creature, bot_skill, self.player, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player, self.player_creature, player_skill, self.bot_player, self.bot_creature)
        else:
            # Random decision when speeds are equal
            if random.choice([True, False]):
                self._execute_skill(self.player, self.player_creature, player_skill, self.bot_player, self.bot_creature)
                if self.bot_creature.hp > 0:
                    self._execute_skill(self.bot_player, self.bot_creature, bot_skill, self.player, self.player_creature)
            else:
                self._execute_skill(self.bot_player, self.bot_creature, bot_skill, self.player, self.player_creature)
                if self.player_creature.hp > 0:
                    self._execute_skill(self.player, self.player_creature, player_skill, self.bot_player, self.bot_creature)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        damage = self._calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        weakness_factor = self._get_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        return final_damage

    def _get_weakness_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal" or defender_type == "normal":
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
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _transition_to_scene(self, scene_name: str):
        self._reset_creatures()
        super()._transition_to_scene(scene_name)

    def _reset_creatures(self):
        for creature in self.player.creatures + self.bot_player.creatures:
            creature.hp = creature.max_hp
