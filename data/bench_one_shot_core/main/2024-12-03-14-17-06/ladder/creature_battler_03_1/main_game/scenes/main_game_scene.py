from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
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

    def execute_turn(self, first_creature, second_creature, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        
        if second_creature.hp <= 0:
            return
            
        # Second attack
        damage = self.calculate_damage(second_creature, first_creature, second_skill)
        first_creature.hp -= damage
        self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_skill = self._wait_for_choice(self.player, skill_choices).thing
            
            # Bot choice phase
            bot_skill = self._wait_for_choice(self.opponent, 
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing
            
            # Determine order
            if self.player_creature.speed > self.opponent_creature.speed:
                first = (self.player_creature, player_skill)
                second = (self.opponent_creature, bot_skill)
            elif self.player_creature.speed < self.opponent_creature.speed:
                first = (self.opponent_creature, bot_skill)
                second = (self.player_creature, player_skill)
            else:
                if random.random() < 0.5:
                    first = (self.player_creature, player_skill)
                    second = (self.opponent_creature, bot_skill)
                else:
                    first = (self.opponent_creature, bot_skill)
                    second = (self.player_creature, player_skill)
                    
            # Execute turn
            self.execute_turn(first[0], second[0], first[1], second[1])
            
            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene") 
                return
