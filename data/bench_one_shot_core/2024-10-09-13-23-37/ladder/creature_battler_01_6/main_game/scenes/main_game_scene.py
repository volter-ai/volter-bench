from typing import List

from main_game.models import Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}

Skill Queue: {', '.join(skill.display_name for skill in self.skill_queue)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self._show_text(self.opponent, f"You encountered {self.player.display_name}'s {self.player_creature.display_name}!")

        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append(choice.thing)

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.skill_queue.append(choice.thing)

    def resolution_phase(self):
        while self.skill_queue:
            skill = self.skill_queue.pop(0)
            if skill in self.player_creature.skills:
                attacker, defender = self.player, self.opponent
                attacker_creature, defender_creature = self.player_creature, self.opponent_creature
            else:
                attacker, defender = self.opponent, self.player
                attacker_creature, defender_creature = self.opponent_creature, self.player_creature

            self._show_text(attacker, f"Your {attacker_creature.display_name} used {skill.display_name}!")
            self._show_text(defender, f"Opponent's {attacker_creature.display_name} used {skill.display_name}!")

            defender_creature.hp -= skill.damage

            self._show_text(attacker, f"You dealt {skill.damage} damage!")
            self._show_text(defender, f"You received {skill.damage} damage!")

            if self.check_battle_end():
                break

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "Your creature fainted. You lost!")
            self._show_text(self.opponent, "You won!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.opponent, "Your creature fainted. You lost!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
