from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_choice = None
        self.opponent_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player choice phase
            self.player_choice = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])

            # Opponent choice phase  
            self.opponent_choice = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills])

            # Resolution phase
            first, second = self.determine_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                break
                
            self.execute_turn(second)
            
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_choice.thing), (self.opponent, self.opponent_choice.thing)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_choice.thing), (self.player, self.player_choice.thing)
        else:
            actors = [(self.player, self.player_choice.thing), (self.opponent, self.opponent_choice.thing)]
            random.shuffle(actors)
            return actors[0], actors[1]

    def calculate_damage(self, attacker, skill, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        factor = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf":
                factor = 2.0
            elif defender.creature_type == "water":
                factor = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire":
                factor = 2.0
            elif defender.creature_type == "leaf":
                factor = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water":
                factor = 2.0
            elif defender.creature_type == "fire":
                factor = 0.5

        return int(raw_damage * factor)

    def execute_turn(self, turn_data):
        actor, skill = turn_data
        attacker = self.player_creature if actor == self.player else self.opponent_creature
        defender = self.opponent_creature if actor == self.player else self.player_creature
        
        damage = self.calculate_damage(attacker, skill, defender)
        defender.hp = max(0, defender.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
        self._show_text(self.opponent, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

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
