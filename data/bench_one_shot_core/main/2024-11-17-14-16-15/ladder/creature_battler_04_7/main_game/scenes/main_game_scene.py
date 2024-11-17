from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
from main_game.models import Skill, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self._reset_creatures()

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def _execute_turn(self, first_creature: Creature, second_creature: Creature, 
                     first_skill: Skill, second_skill: Skill):
        # First attack
        damage = self._calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp = max(0, second_creature.hp - damage)
        self._show_text(self.player, 
            f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")

        if second_creature.hp > 0:
            # Second attack
            damage = self._calculate_damage(second_creature, first_creature, second_skill)
            first_creature.hp = max(0, first_creature.hp - damage)
            self._show_text(self.player,
                f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectSkill(skill) for skill in self.player_creature.skills]).skill

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectSkill(skill) for skill in self.opponent_creature.skills]).skill

            # Determine order
            if self.player_creature.speed > self.opponent_creature.speed:
                first = (self.player_creature, player_skill)
                second = (self.opponent_creature, opponent_skill)
            elif self.player_creature.speed < self.opponent_creature.speed:
                first = (self.opponent_creature, opponent_skill)
                second = (self.player_creature, player_skill)
            else:
                if random.random() < 0.5:
                    first = (self.player_creature, player_skill)
                    second = (self.opponent_creature, opponent_skill)
                else:
                    first = (self.opponent_creature, opponent_skill)
                    second = (self.player_creature, player_skill)

            # Execute turn
            self._execute_turn(first[0], second[0], first[1], second[1])

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

class SelectSkill(DictionaryChoice):
    def __init__(self, skill: Skill):
        super().__init__(display_name=skill.display_name)
        self.skill = skill
