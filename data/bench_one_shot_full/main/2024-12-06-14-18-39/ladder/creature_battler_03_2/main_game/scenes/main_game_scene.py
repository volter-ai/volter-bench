from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} - {skill.base_damage} damage)" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        type_effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": type_effectiveness = 2.0
            elif defender.creature_type == "water": type_effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": type_effectiveness = 2.0
            elif defender.creature_type == "leaf": type_effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": type_effectiveness = 2.0
            elif defender.creature_type == "fire": type_effectiveness = 0.5
            
        return int(raw_damage * type_effectiveness)

    def execute_turn(self, first_creature, second_creature, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        
        # Second attack (if still alive)
        if second_creature.hp > 0:
            damage = self.calculate_damage(second_creature, first_creature, second_skill)
            first_creature.hp -= damage
            self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, player_skill_choices)
            player_skill = next(skill for skill in self.player_creature.skills 
                              if skill.display_name == player_choice.display_name)

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(self.opponent, 
                [Button(skill.display_name) for skill in self.opponent_creature.skills])
            opponent_skill = next(skill for skill in self.opponent_creature.skills 
                                if skill.display_name == opponent_skill.display_name)

            # Resolution phase
            if self.player_creature.speed > self.opponent_creature.speed:
                first = (self.player_creature, self.opponent_creature, player_skill, opponent_skill)
            elif self.player_creature.speed < self.opponent_creature.speed:
                first = (self.opponent_creature, self.player_creature, opponent_skill, player_skill)
            else:
                if random.random() < 0.5:
                    first = (self.player_creature, self.opponent_creature, player_skill, opponent_skill)
                else:
                    first = (self.opponent_creature, self.player_creature, opponent_skill, player_skill)
                    
            self.execute_turn(*first)

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._quit_whole_game()  # Properly end the game after victory
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._quit_whole_game()  # Properly end the game after defeat
