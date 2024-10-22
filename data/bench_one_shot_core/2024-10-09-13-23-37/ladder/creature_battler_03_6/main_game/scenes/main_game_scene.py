import random

from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self._show_text(self.opponent, f"You're battling against {self.player_creature.display_name}!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            player_skill = self.player_turn()
            opponent_skill = self.opponent_turn()

            first, second = self.determine_turn_order(player_skill, opponent_skill)
            self.execute_turn(first)
            if self.check_battle_end():
                break
            self.execute_turn(second)
            if self.check_battle_end():
                break

    def player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def determine_turn_order(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, player_skill), (self.opponent, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, opponent_skill), (self.player, player_skill)
        else:
            if random.random() < 0.5:
                return (self.player, player_skill), (self.opponent, opponent_skill)
            else:
                return (self.opponent, opponent_skill), (self.player, player_skill)

    def execute_turn(self, turn):
        attacker, skill = turn
        if attacker == self.player:
            defender = self.opponent
            attacker_creature = self.player_creature
            defender_creature = self.opponent_creature
        else:
            defender = self.player
            attacker_creature = self.opponent_creature
            defender_creature = self.player_creature

        damage = self.calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")
        self._show_text(self.opponent, f"{defender_creature.display_name} took {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = raw_damage * type_factor
        return int(final_damage)  # Convert to integer only at the final step

    def get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire":
            if defender_type == "leaf":
                return 2.0
            elif defender_type == "water":
                return 0.5
        elif skill_type == "water":
            if defender_type == "fire":
                return 2.0
            elif defender_type == "leaf":
                return 0.5
        elif skill_type == "leaf":
            if defender_type == "water":
                return 2.0
            elif defender_type == "fire":
                return 0.5
        return 1.0

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
