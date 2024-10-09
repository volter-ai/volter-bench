from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


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

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self, player_skill, foe_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            # Equal speeds, randomly choose who goes first
            first, second = random.choice([(self.player, self.opponent), (self.opponent, self.player)])
            first_creature = self.player_creature if first == self.player else self.opponent_creature
            second_creature = self.opponent_creature if first == self.player else self.player_creature
            first_skill = player_skill if first == self.player else foe_skill
            second_skill = foe_skill if first == self.player else player_skill

            self.execute_skill(first, first_creature, first_skill, second_creature)
            if second_creature.hp > 0:
                self.execute_skill(second, second_creature, second_skill, first_creature)

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}! It dealt {final_damage} damage.")

    def calculate_weakness_factor(self, skill_type, defender_type):
        type_relationships = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 1, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 1, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 1}
        }
        return type_relationships[skill_type][defender_type]

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self.end_battle(f"Your {self.player_creature.display_name} fainted. You lost!")
            return True
        elif self.opponent_creature.hp <= 0:
            self.end_battle(f"Opponent's {self.opponent_creature.display_name} fainted. You won!")
            return True
        return False

    def end_battle(self, message):
        self._show_text(self.player, message)
        self._transition_to_scene("MainMenuScene")
