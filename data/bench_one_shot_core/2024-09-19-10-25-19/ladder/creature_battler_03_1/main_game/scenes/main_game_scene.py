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
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}

Opponent's skills:
{', '.join([skill.display_name for skill in self.opponent_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild opponent appears!")
        self._show_text(self.opponent, "A challenger approaches!")

        while True:
            if self.battle_round():
                break

    def battle_round(self):
        player_skill = self.player_choice_phase()
        opponent_skill = self.foe_choice_phase()
        return self.resolution_phase(player_skill, opponent_skill)

    def player_choice_phase(self):
        self._show_text(self.player, f"Your turn to choose a skill:")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} is choosing a skill...")
        self._show_text(self.player, f"Opponent's skills: {', '.join([skill.display_name for skill in self.opponent_creature.skills])}")
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} has chosen a skill!")
        return choice.thing

    def resolution_phase(self, player_skill, opponent_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        if self.execute_skill(first, second, first_skill):
            return True
        if self.execute_skill(second, first, second_skill):
            return True
        return False

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def execute_skill(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_factor = self.calculate_weakness(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} takes {final_damage} damage!")

        if defender.hp == 0:
            winner = self.player if defender == self.opponent_creature else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def calculate_weakness(self, skill_type, creature_type):
        weaknesses = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5},
            "normal": {}  # Normal type is neither effective nor ineffective against any type
        }
        return weaknesses.get(skill_type, {}).get(creature_type, 1)
