from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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

    def calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        multiplier = 1.0
        if skill.skill_type != "normal":
            if (skill.skill_type == "fire" and defender.creature_type == "leaf") or \
               (skill.skill_type == "water" and defender.creature_type == "fire") or \
               (skill.skill_type == "leaf" and defender.creature_type == "water"):
                multiplier = 2.0
            elif (skill.skill_type == "fire" and defender.creature_type == "water") or \
                 (skill.skill_type == "water" and defender.creature_type == "leaf") or \
                 (skill.skill_type == "leaf" and defender.creature_type == "fire"):
                multiplier = 0.5

        return int(raw_damage * multiplier)

    def execute_turn(self, first, second, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first, second, first_skill)
        second.hp -= damage
        self._show_text(self.player, f"{first.display_name} used {first_skill.display_name} for {damage} damage!")
        
        # Second attack if still alive
        if second.hp > 0:
            damage = self.calculate_damage(second, first, second_skill)
            first.hp -= damage
            self._show_text(self.player, f"{second.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Resolution phase
            if self.player_creature.speed > self.opponent_creature.speed or \
               (self.player_creature.speed == self.opponent_creature.speed and random.random() < 0.5):
                self.execute_turn(self.player_creature, self.opponent_creature, player_skill, opponent_skill)
            else:
                self.execute_turn(self.opponent_creature, self.player_creature, opponent_skill, player_skill)

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")
