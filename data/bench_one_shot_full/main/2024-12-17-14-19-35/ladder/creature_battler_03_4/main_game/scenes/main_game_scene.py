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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def calculate_damage(self, skill, attacker, defender):
        # Convert all values to float for calculation
        attack = float(attacker.attack)
        base_damage = float(skill.base_damage)
        defense = float(defender.defense)
        
        # Calculate raw damage using floats
        raw_damage = attack + base_damage - defense
        
        # Type effectiveness (using float multipliers)
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
            
        # Calculate final damage and convert to int only at the end
        return int(raw_damage * multiplier)

    def execute_turn(self, first_creature, first_skill, second_creature, second_skill):
        # First attack
        damage = self.calculate_damage(first_skill, first_creature, second_creature)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        
        # Second attack if still alive
        if second_creature.hp > 0:
            damage = self.calculate_damage(second_skill, second_creature, first_creature)
            first_creature.hp -= damage
            self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_skill = self._wait_for_choice(self.player, choices).thing
            
            # Opponent choice phase
            opponent_skill = self._wait_for_choice(self.opponent, 
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing
            
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
            self.execute_turn(first[0], first[1], second[0], second[1])
            
            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._quit_whole_game()
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._quit_whole_game()
