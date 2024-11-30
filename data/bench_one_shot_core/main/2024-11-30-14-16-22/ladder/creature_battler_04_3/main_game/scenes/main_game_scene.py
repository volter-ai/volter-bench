from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
        # Reset creature stats
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
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
        # Determine order
        first = self.player_creature if self.player_creature.speed > self.opponent_creature.speed else self.opponent_creature
        second = self.opponent_creature if first == self.player_creature else self.player_creature
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill
        
        # If speeds are equal, randomize
        if self.player_creature.speed == self.opponent_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                first_skill, second_skill = second_skill, first_skill

        # Execute first attack
        if first == self.player_creature:
            damage = self.calculate_damage(self.player_creature, self.opponent_creature, first_skill)
            self.opponent_creature.hp -= damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        else:
            damage = self.calculate_damage(self.opponent_creature, self.player_creature, first_skill)
            self.player_creature.hp -= damage
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {first_skill.display_name} for {damage} damage!")

        # Check if battle is over
        if self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0:
            return

        # Execute second attack
        if second == self.player_creature:
            damage = self.calculate_damage(self.player_creature, self.opponent_creature, second_skill)
            self.opponent_creature.hp -= damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {second_skill.display_name} for {damage} damage!")
        else:
            damage = self.calculate_damage(self.opponent_creature, self.player_creature, second_skill)
            self.player_creature.hp -= damage
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_skill = self._wait_for_choice(self.player, player_choices).thing

            # Opponent choice phase
            opponent_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
            opponent_skill = self._wait_for_choice(self.opponent, opponent_choices).thing

            # Resolution phase
            self.execute_turn(player_skill, opponent_skill)

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")
