from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
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

    def execute_turn(self, first, second, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first, second, first_skill)
        second.hp -= damage
        self._show_text(self.player, f"{first.display_name} used {first_skill.display_name}!")
        self._show_text(self.player, f"Dealt {damage} damage!")

        # Check if battle ended
        if second.hp <= 0:
            return True

        # Second attack
        damage = self.calculate_damage(second, first, second_skill)
        first.hp -= damage
        self._show_text(self.player, f"{second.display_name} used {second_skill.display_name}!")
        self._show_text(self.player, f"Dealt {damage} damage!")

        return first.hp <= 0

    def run(self):
        while True:
            # Player choice
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            player_skill = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)

            # Opponent choice
            opponent_choice = self._wait_for_choice(self.opponent, [Button(skill.display_name) for skill in self.opponent_creature.skills])
            opponent_skill = next(s for s in self.opponent_creature.skills if s.display_name == opponent_choice.display_name)

            # Determine order
            if self.player_creature.speed > self.opponent_creature.speed:
                first, second = self.player_creature, self.opponent_creature
                first_skill, second_skill = player_skill, opponent_skill
            elif self.player_creature.speed < self.opponent_creature.speed:
                first, second = self.opponent_creature, self.player_creature
                first_skill, second_skill = opponent_skill, player_skill
            else:
                if random.random() < 0.5:
                    first, second = self.player_creature, self.opponent_creature
                    first_skill, second_skill = player_skill, opponent_skill
                else:
                    first, second = self.opponent_creature, self.player_creature
                    first_skill, second_skill = opponent_skill, player_skill

            # Execute turn
            battle_ended = self.execute_turn(first, second, first_skill, second_skill)

            if battle_ended:
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lost!")
                else:
                    self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return
