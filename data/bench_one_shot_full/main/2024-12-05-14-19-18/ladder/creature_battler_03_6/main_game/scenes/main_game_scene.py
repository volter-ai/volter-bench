from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
import math

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_skills = {}

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        type_multipliers = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        multiplier = type_multipliers.get((skill.skill_type, defender.creature_type), 1.0)
        return int(raw_damage * multiplier)

    def execute_turn(self):
        creatures = [(self.player_creature, self.queued_skills[self.player.uid]), 
                    (self.opponent_creature, self.queued_skills[self.opponent.uid])]
        
        # Sort by speed, randomize if equal
        creatures.sort(key=lambda x: (x[0].speed, random.random()), reverse=True)
        
        for attacker, skill in creatures:
            if attacker == self.player_creature:
                defender = self.opponent_creature
                attacker_name = self.player.display_name
            else:
                defender = self.player_creature
                attacker_name = self.opponent.display_name
                
            damage = self.calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker_name}'s {attacker.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"It dealt {damage} damage!")
            
            if defender.hp <= 0:
                return True
        return False

    def run(self):
        while True:
            # Player choice phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.queued_skills[self.player.uid] = player_choice.thing
            
            # Opponent choice phase
            opponent_choice = self._wait_for_choice(self.opponent, 
                [SelectThing(skill) for skill in self.opponent_creature.skills])
            self.queued_skills[self.opponent.uid] = opponent_choice.thing
            
            # Resolution phase
            battle_ended = self.execute_turn()
            
            if battle_ended:
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lost!")
                else:
                    self._show_text(self.player, "You won!")
                    
                # After showing battle result, give player choice to return to menu or quit
                continue_button = Button("Return to Main Menu")
                quit_button = Button("Quit Game")
                choice = self._wait_for_choice(self.player, [continue_button, quit_button])
                
                if choice == continue_button:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
