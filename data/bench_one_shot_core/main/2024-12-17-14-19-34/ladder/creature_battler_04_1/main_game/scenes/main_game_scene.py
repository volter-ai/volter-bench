from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.reset_creatures()

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                multiplier = 2.0
            elif defender_creature.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                multiplier = 2.0
            elif defender_creature.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                multiplier = 2.0
            elif defender_creature.creature_type == "fire":
                multiplier = 0.5

        return int(raw_damage * multiplier)

    def execute_turn(self, player_skill, opponent_skill):
        # Determine order
        player_first = True
        if self.opponent_creature.speed > self.player_creature.speed:
            player_first = False
        elif self.opponent_creature.speed == self.player_creature.speed:
            player_first = random.choice([True, False])

        if player_first:
            # Player attacks first
            damage = self.calculate_damage(self.player_creature, self.opponent_creature, player_skill)
            self.opponent_creature.hp = max(0, self.opponent_creature.hp - damage)
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name} for {damage} damage!")
            
            if self.opponent_creature.hp > 0:
                # Opponent attacks second
                damage = self.calculate_damage(self.opponent_creature, self.player_creature, opponent_skill)
                self.player_creature.hp = max(0, self.player_creature.hp - damage)
                self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name} for {damage} damage!")
        else:
            # Opponent attacks first
            damage = self.calculate_damage(self.opponent_creature, self.player_creature, opponent_skill)
            self.player_creature.hp = max(0, self.player_creature.hp - damage)
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name} for {damage} damage!")
            
            if self.player_creature.hp > 0:
                # Player attacks second
                damage = self.calculate_damage(self.player_creature, self.opponent_creature, player_skill)
                self.opponent_creature.hp = max(0, self.opponent_creature.hp - damage)
                self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name} for {damage} damage!")

    def run(self):
        self._show_text(self.player, f"Battle Start! Your {self.player_creature.display_name} vs opponent's {self.opponent_creature.display_name}!")

        while True:
            # Player choice phase
            player_skill_buttons = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, player_skill_buttons)
            player_skill = next(skill for skill in self.player_creature.skills 
                              if skill.display_name == player_choice.display_name)

            # Opponent choice phase
            opponent_skill_buttons = [Button(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_skill_buttons)
            opponent_skill = next(skill for skill in self.opponent_creature.skills 
                                if skill.display_name == opponent_choice.display_name)

            # Resolution phase
            self.execute_turn(player_skill, opponent_skill)

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break
