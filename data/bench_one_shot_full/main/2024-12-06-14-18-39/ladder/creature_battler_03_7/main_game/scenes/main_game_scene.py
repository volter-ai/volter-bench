from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.player_chosen_skill = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)

            # Opponent choice phase
            self._show_text(self.opponent, "Choose your skill!")
            opponent_skill_choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_skill_choices)
            self.opponent_chosen_skill = next(s for s in self.opponent_creature.skills if s.display_name == opponent_choice.display_name)

            # Resolution phase
            first, second = self.determine_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                continue  # This will now handle the transition
                
            self.execute_turn(second)
            self.check_battle_end()

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_chosen_skill), (self.opponent, self.opponent_chosen_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_chosen_skill), (self.player, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_chosen_skill), (self.opponent, self.opponent_chosen_skill)
            return (self.opponent, self.opponent_chosen_skill), (self.player, self.player_chosen_skill)

    def calculate_damage(self, attacker, skill, defender):
        raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        
        # Type effectiveness
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

    def execute_turn(self, turn_data):
        attacker, skill = turn_data
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.opponent_creature
        else:
            attacker_creature = self.opponent_creature
            defender_creature = self.player_creature

        damage = self.calculate_damage(attacker_creature, skill, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
