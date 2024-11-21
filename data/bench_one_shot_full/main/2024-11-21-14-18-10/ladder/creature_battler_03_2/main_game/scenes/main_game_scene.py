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
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, choices)
            self.player_chosen_skill = next(s for s in self.player_creature.skills 
                                          if s.display_name == choice.display_name)

            # Opponent choice phase
            self._show_text(self.opponent, "Choose your skill!")
            opponent_choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_choices)
            self.opponent_chosen_skill = next(s for s in self.opponent_creature.skills 
                                            if s.display_name == opponent_choice.display_name)

            # Resolution phase
            first, second = self.determine_order()
            self.execute_turn(first)
            if not self.check_battle_end():
                self.execute_turn(second)
                if self.check_battle_end():
                    break
            else:
                break

        self._transition_to_scene("MainMenuScene")

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
        raw_damage = attacker.creatures[0].attack + skill.base_damage - defender.creatures[0].defense
        
        # Type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creatures[0].creature_type == "leaf":
                effectiveness = 2.0
            elif defender.creatures[0].creature_type == "water":
                effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creatures[0].creature_type == "fire":
                effectiveness = 2.0
            elif defender.creatures[0].creature_type == "leaf":
                effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creatures[0].creature_type == "water":
                effectiveness = 2.0
            elif defender.creatures[0].creature_type == "fire":
                effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def execute_turn(self, turn_data):
        attacker, skill = turn_data
        defender = self.opponent if attacker == self.player else self.player
        
        damage = self.calculate_damage(attacker, skill, defender)
        defender.creatures[0].hp = max(0, defender.creatures[0].hp - damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name}! "
            f"Dealt {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
