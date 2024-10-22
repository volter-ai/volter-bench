from typing import List, Tuple

from main_game.models import Creature, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[Tuple[Creature, Creature, Skill]] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{self.get_skill_list(self.player_creature)}
"""

    def get_skill_list(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            self.skill_queue.clear()

            # Player Choice Phase
            self.player_choice_phase()

            # Foe Choice Phase
            self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase()

            # Check for battle end
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        skill = next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)
        self.skill_queue.append((self.player_creature, self.foe_creature, skill))

    def foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        skill = next(skill for skill in self.foe_creature.skills if skill.display_name == choice.display_name)
        self.skill_queue.append((self.foe_creature, self.player_creature, skill))

    def resolution_phase(self):
        for attacker, defender, skill in self.skill_queue:
            defender.hp -= skill.damage
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
            self._show_text(self.foe, f"{attacker.display_name} used {skill.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.foe.creatures:
            creature.hp = creature.max_hp
