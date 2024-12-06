from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            self._show_text(self.player, "Choose your skill!")
            self.player_chosen_skill = self._wait_for_choice(
                self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent Choice Phase
            self._show_text(self.opponent, "Choose your skill!")
            self.opponent_chosen_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution Phase
            first, second = self.determine_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                break
                
            self.execute_turn(second)
            
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_chosen_skill), (self.opponent, self.opponent_chosen_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            return (self.opponent, self.opponent_chosen_skill), (self.player, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_chosen_skill), (self.opponent, self.opponent_chosen_skill)
            return (self.opponent, self.opponent_chosen_skill), (self.player, self.player_chosen_skill)

    def calculate_damage(self, attacker, skill, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def execute_turn(self, turn_data):
        attacker, skill = turn_data
        defender = self.opponent if attacker == self.player else self.player
        attacker_creature = self.player_creature if attacker == self.player else self.opponent_creature
        defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
        
        damage = self.calculate_damage(attacker_creature, skill, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
