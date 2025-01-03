from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
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

    def execute_turn(self, first_creature, second_creature, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        
        # Check if battle ended
        if second_creature.hp <= 0:
            return
            
        # Second attack
        damage = self.calculate_damage(second_creature, first_creature, second_skill)
        first_creature.hp -= damage
        self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices).thing
            
            # Opponent choice phase
            opponent_choice = self._wait_for_choice(self.opponent, 
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing
            
            # Determine order
            if self.player_creature.speed > self.opponent_creature.speed:
                first = (self.player_creature, player_choice)
                second = (self.opponent_creature, opponent_choice)
            elif self.player_creature.speed < self.opponent_creature.speed:
                first = (self.opponent_creature, opponent_choice)
                second = (self.player_creature, player_choice)
            else:
                if random.random() < 0.5:
                    first = (self.player_creature, player_choice)
                    second = (self.opponent_creature, opponent_choice)
                else:
                    first = (self.opponent_creature, opponent_choice)
                    second = (self.player_creature, player_choice)
                    
            # Execute turn
            self.execute_turn(first[0], second[0], first[1], second[1])
            
            # Check win conditions
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._quit_whole_game()  # Properly end the game instead of breaking
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._quit_whole_game()  # Properly end the game instead of breaking
