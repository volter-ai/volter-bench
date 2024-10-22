from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_skill = None
        self.opponent_skill = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.game_loop()

    def game_loop(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill = choice.thing

    def resolution_phase(self):
        first, second = self.determine_order()
        self.execute_skill(first)
        if not self.check_battle_end():
            self.execute_skill(second)

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_skill), (self.opponent, self.opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_skill), (self.player, self.player_skill)
        else:
            if random.choice([True, False]):
                return (self.player, self.player_skill), (self.opponent, self.opponent_skill)
            else:
                return (self.opponent, self.opponent_skill), (self.player, self.player_skill)

    def execute_skill(self, attacker_info):
        attacker, skill = attacker_info
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.opponent_creature
        else:
            attacker_creature = self.opponent_creature
            defender_creature = self.player_creature

        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(damage, 0)  # Ensure damage is not negative
        defender_creature.hp -= damage

        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
