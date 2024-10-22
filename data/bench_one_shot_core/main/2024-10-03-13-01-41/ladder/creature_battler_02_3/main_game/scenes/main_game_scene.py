from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your turn:
{self.get_skill_choices()}
"""

    def get_skill_choices(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            player_skill = self.player_choice_phase()
            foe_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, foe_skill)

            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return next(skill for skill in self.foe_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self, player_skill, foe_skill):
        first, second = self.determine_order()
        self.execute_skill(first, second, player_skill if first == self.player else foe_skill)
        if self.check_battle_end():
            return
        self.execute_skill(second, first, foe_skill if first == self.player else player_skill)

    def determine_order(self):
        if self.player_creature.speed > self.foe_creature.speed:
            return self.player, self.foe
        elif self.player_creature.speed < self.foe_creature.speed:
            return self.foe, self.player
        else:
            return random.sample([self.player, self.foe], 2)

    def execute_skill(self, attacker, defender, skill):
        attacker_creature = attacker.creatures[0]
        defender_creature = defender.creatures[0]
        damage = max(0, attacker_creature.attack + skill.base_damage - defender_creature.defense)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted. You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} fainted. You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
