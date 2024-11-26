from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
from main_game.models import Skill
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
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}"""

    def _calculate_damage(self, attacker_creature, defender_creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf": multiplier = 2.0
            elif defender_creature.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire": multiplier = 2.0
            elif defender_creature.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water": multiplier = 2.0
            elif defender_creature.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def _get_skill_from_choices(self, creature, player) -> Skill:
        # Create mapping of display names to skills
        skill_map = {skill.display_name: skill for skill in creature.skills}
        
        # Create choices using display names
        skill_choices = [DictionaryChoice(name) for name in skill_map.keys()]
        
        # Get choice and look up corresponding skill
        choice = self._wait_for_choice(player, skill_choices)
        return skill_map[choice.display_name]

    def _execute_turn(self, first_creature, second_creature, first_skill, second_skill):
        # First attack
        damage = self._calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        
        if second_creature.hp <= 0:
            return

        # Second attack
        damage = self._calculate_damage(second_creature, first_creature, second_skill)
        first_creature.hp -= damage
        self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def _determine_turn_order(self):
        # If speeds are equal, randomly choose who goes first
        if self.player_creature.speed == self.opponent_creature.speed:
            return (self.player_creature, self.opponent_creature) if random.random() < 0.5 else (self.opponent_creature, self.player_creature)
        # Otherwise use speed to determine order
        return (self.player_creature, self.opponent_creature) if self.player_creature.speed > self.opponent_creature.speed else (self.opponent_creature, self.player_creature)

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._get_skill_from_choices(self.player_creature, self.player)

            # Opponent choice phase
            opponent_skill = self._get_skill_from_choices(self.opponent_creature, self.opponent)

            # Resolution phase - determine turn order
            first_creature, second_creature = self._determine_turn_order()
            first_skill = player_skill if first_creature == self.player_creature else opponent_skill
            second_skill = opponent_skill if first_creature == self.player_creature else player_skill

            # Execute turn with determined order
            self._execute_turn(first_creature, second_creature, first_skill, second_skill)

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")
