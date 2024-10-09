from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


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

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        battle_result = None
        while not battle_result:
            # Player Choice Phase
            player_skill = self.player_choice_phase()

            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)

            # Check for battle end condition
            battle_result = self.check_battle_end()

        self.display_battle_result(battle_result)
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, foe_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else foe_skill
        second_skill = foe_skill if first == self.player_creature else player_skill

        self.execute_skill(first, second, first_skill)
        if second.hp > 0:
            self.execute_skill(second, first, second_skill)

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def execute_skill(self, attacker, defender, skill):
        damage = max(0, attacker.attack + skill.base_damage - defender.defense)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} and dealt {damage} damage to {defender.display_name}!")
        self._show_text(self.opponent, f"{attacker.display_name} used {skill.display_name} and dealt {damage} damage to {defender.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            return "lose"
        elif self.opponent_creature.hp <= 0:
            return "win"
        return None

    def display_battle_result(self, result):
        if result == "win":
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
        else:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
