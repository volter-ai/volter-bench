from mini_game_engine.engine.lib import AbstractGameScene, Button
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
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._foe_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            if self._check_battle_end():
                self._transition_to_scene("MainMenuScene")
                break

    def _player_choice_phase(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self, opponent, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(opponent, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, foe_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
        else:
            # If speeds are equal, randomly decide who goes first
            first_attacker, first_creature, first_skill, second_attacker, second_creature, second_skill = random.choice([
                (self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature, foe_skill),
                (self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature, player_skill)
            ])
            self._execute_skill(first_attacker, first_creature, first_skill, second_attacker, second_creature)
            if second_creature.hp > 0:
                self._execute_skill(second_attacker, second_creature, second_skill, first_attacker, first_creature)

    def _execute_skill(self, attacker, attacker_creature, skill, defender, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1
        elif skill_type == "fire" and defender_type == "leaf":
            return 2
        elif skill_type == "fire" and defender_type == "water":
            return 0.5
        elif skill_type == "water" and defender_type == "fire":
            return 2
        elif skill_type == "water" and defender_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and defender_type == "water":
            return 2
        elif skill_type == "leaf" and defender_type == "fire":
            return 0.5
        else:
            return 1

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
