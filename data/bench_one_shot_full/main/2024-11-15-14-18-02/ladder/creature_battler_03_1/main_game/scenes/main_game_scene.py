from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
import math

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
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
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

    def execute_turn(self, first, second, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first, second, first_skill)
        second.hp = max(0, second.hp - damage)
        self._show_text(self.player, f"{first.display_name} used {first_skill.display_name} for {damage} damage!")
        
        if second.hp > 0:
            # Second attack
            damage = self.calculate_damage(second, first, second_skill)
            first.hp = max(0, first.hp - damage)
            self._show_text(self.player, f"{second.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            
            # Bot choice phase
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills])

            # Resolution phase
            if self.player_creature.speed > self.opponent_creature.speed:
                first = self.player_creature
                second = self.opponent_creature
                first_skill = player_skill.thing
                second_skill = opponent_skill.thing
            elif self.player_creature.speed < self.opponent_creature.speed:
                first = self.opponent_creature
                second = self.player_creature
                first_skill = opponent_skill.thing
                second_skill = player_skill.thing
            else:
                if random.random() < 0.5:
                    first = self.player_creature
                    second = self.opponent_creature
                    first_skill = player_skill.thing
                    second_skill = opponent_skill.thing
                else:
                    first = self.opponent_creature
                    second = self.player_creature
                    first_skill = opponent_skill.thing
                    second_skill = player_skill.thing

            self.execute_turn(first, second, first_skill, second_skill)

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene")
                return
