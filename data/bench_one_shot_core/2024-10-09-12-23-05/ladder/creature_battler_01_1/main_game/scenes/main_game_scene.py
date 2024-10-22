from typing import List, Tuple

from main_game.models import Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.skill_queue: List[Tuple[Player, Skill]] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}

Skill queue: {', '.join(skill.display_name for _, skill in self.skill_queue)}
"""

    def run(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append((self.player, choice.thing))

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        self.skill_queue.append((self.bot, choice.thing))

    def resolution_phase(self):
        while self.skill_queue:
            attacker, skill = self.skill_queue.pop(0)
            defender = self.bot if attacker == self.player else self.player
            defender_creature = self.bot_creature if attacker == self.player else self.player_creature

            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
            self._show_text(self.bot, f"{attacker.display_name} used {skill.display_name}!")
            
            defender_creature.hp = max(0, defender_creature.hp - skill.damage)
            self._show_text(self.player, f"Dealt {skill.damage} damage to {defender.display_name}'s creature!")
            self._show_text(self.bot, f"Dealt {skill.damage} damage to {defender.display_name}'s creature!")

            if self.check_battle_end():
                break

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.bot, "You won the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.bot, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self.skill_queue.clear()
