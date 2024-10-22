from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[Skill] = []

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
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appears!")
        self.battle_loop()
        self._transition_to_scene("MainMenuScene")  # Return to main menu after battle

    def battle_loop(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

            if self.check_battle_end():
                break

        self.reset_creatures()

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append(choice.thing)

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.skill_queue.append(choice.thing)

    def resolution_phase(self):
        while self.skill_queue:
            skill = self.skill_queue.pop(0)
            if skill in self.player_creature.skills:
                self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} uses {skill.display_name}!")
                self.foe_creature.hp = max(0, self.foe_creature.hp - skill.damage)
            else:
                self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} uses {skill.display_name}!")
                self.player_creature.hp = max(0, self.player_creature.hp - skill.damage)
            
            if self.check_battle_end():
                break

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} fainted! You win!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
        self.skill_queue.clear()
