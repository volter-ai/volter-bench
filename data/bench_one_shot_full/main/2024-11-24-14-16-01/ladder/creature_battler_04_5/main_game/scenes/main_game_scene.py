from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
        # Reset creatures to full HP
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * effectiveness)
        return max(1, final_damage)  # Minimum 1 damage

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5, "fire": 1.0},
            "water": {"fire": 2.0, "leaf": 0.5, "water": 1.0},
            "leaf": {"water": 2.0, "fire": 0.5, "leaf": 1.0}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

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
            player_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_skill = self._wait_for_choice(self.player, player_choices).thing
            
            # Bot choice phase
            bot_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
            bot_skill = self._wait_for_choice(self.opponent, bot_choices).thing
            
            # Determine order
            if self.player_creature.speed > self.opponent_creature.speed:
                first = (self.player_creature, self.opponent_creature, player_skill, bot_skill)
            elif self.player_creature.speed < self.opponent_creature.speed:
                first = (self.opponent_creature, self.player_creature, bot_skill, player_skill)
            else:
                if random.random() < 0.5:
                    first = (self.player_creature, self.opponent_creature, player_skill, bot_skill)
                else:
                    first = (self.opponent_creature, self.player_creature, bot_skill, player_skill)
                    
            # Execute turn
            self.execute_turn(*first)
            
            # Check win conditions
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
                
        self._transition_to_scene("MainMenuScene")
