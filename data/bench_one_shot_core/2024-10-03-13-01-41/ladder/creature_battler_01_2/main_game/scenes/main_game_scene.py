from collections import deque

from main_game.models import Creature
from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue = deque()

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
{self.get_skill_choices_str(self.player_creature)}
"""

    def get_skill_choices_str(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

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
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        skill = next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)
        self.skill_queue.append((self.player, self.player_creature, skill))

    def foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        skill = next(skill for skill in self.foe_creature.skills if skill.display_name == choice.display_name)
        self.skill_queue.append((self.foe, self.foe_creature, skill))

    def resolution_phase(self):
        while self.skill_queue:
            attacker, attacker_creature, skill = self.skill_queue.popleft()
            defender = self.foe if attacker == self.player else self.player
            defender_creature = self.foe_creature if attacker == self.player else self.player_creature

            defender_creature.hp -= skill.damage
            self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
            self._show_text(self.foe, f"{attacker_creature.display_name} used {skill.display_name}!")

            if defender_creature.hp <= 0:
                break

    def check_battle_end(self) -> bool:
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
