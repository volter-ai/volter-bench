from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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
        self._show_text(self.player, f"A battle begins between {self.player.display_name} and {self.opponent.display_name}!")
        
        try:
            while True:
                # Player choice phase
                player_choice = self._wait_for_choice(
                    self.player, 
                    [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
                )
                self.player_chosen_skill = player_choice.thing

                # Opponent choice phase
                opponent_choice = self._wait_for_choice(
                    self.opponent,
                    [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
                )
                self.opponent_chosen_skill = opponent_choice.thing

                # Resolution phase
                first, second = self.determine_order()
                self.execute_turn(first)
                if not self.check_battle_end():
                    self.execute_turn(second)
                    if self.check_battle_end():
                        break
                else:
                    break
        finally:
            # Reset creature states before transitioning
            self.reset_creature_states()
            self._transition_to_scene("MainMenuScene")

    def reset_creature_states(self):
        """Reset all creatures back to their starting state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.choice([(self.player, self.opponent), (self.opponent, self.player)])

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender_creature.creature_type)
        return int(raw_damage * type_factor)

    def get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def execute_turn(self, player):
        attacker = self.player_creature if player == self.player else self.opponent_creature
        defender = self.opponent_creature if player == self.player else self.player_creature
        skill = self.player_chosen_skill if player == self.player else self.opponent_chosen_skill

        damage = self.calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} has been defeated!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name} has been defeated!")
            return True
        return False
