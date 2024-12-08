from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        # Reset creatures to full HP
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

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

    def execute_turn(self, player_skill, opponent_skill):
        # Determine order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player_creature, self.opponent_creature, player_skill)
            second = (self.opponent_creature, self.player_creature, opponent_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            first = (self.opponent_creature, self.player_creature, opponent_skill)
            second = (self.player_creature, self.opponent_creature, player_skill)
        else:
            if random.random() < 0.5:
                first = (self.player_creature, self.opponent_creature, player_skill)
                second = (self.opponent_creature, self.player_creature, opponent_skill)
            else:
                first = (self.opponent_creature, self.player_creature, opponent_skill)
                second = (self.player_creature, self.opponent_creature, player_skill)

        # Execute attacks in order
        for attacker, defender, skill in [first, second]:
            if defender.hp > 0:  # Only attack if defender still alive
                damage = self.calculate_damage(attacker, defender, skill)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        
        while True:
            # Player choice phase
            player_skill_choices = []
            for i, skill in enumerate(self.player_creature.skills):
                choice = DictionaryChoice(skill.display_name)
                choice.value = {"skill_index": i}
                player_skill_choices.append(choice)
            
            player_choice = self._wait_for_choice(self.player, player_skill_choices)
            player_skill = self.player_creature.skills[player_choice.value["skill_index"]]

            # Opponent choice phase
            opponent_skill_choices = []
            for i, skill in enumerate(self.opponent_creature.skills):
                choice = DictionaryChoice(skill.display_name)
                choice.value = {"skill_index": i}
                opponent_skill_choices.append(choice)
            
            opponent_choice = self._wait_for_choice(self.opponent, opponent_skill_choices)
            opponent_skill = self.opponent_creature.skills[opponent_choice.value["skill_index"]]

            # Resolution phase
            self.execute_turn(player_skill, opponent_skill)

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")
