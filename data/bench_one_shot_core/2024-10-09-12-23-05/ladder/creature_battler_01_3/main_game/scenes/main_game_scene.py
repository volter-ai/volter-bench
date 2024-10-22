from typing import List

from main_game.models import Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appears!")
        
        while True:
            self.player_choice_phase()
            self.bot_choice_phase()
            
            self.resolution_phase()
            
            if self.check_battle_end():
                break

        self.reset_creatures()
        
        play_again_button = Button("Play Again")
        main_menu_button = Button("Return to Main Menu")
        choices = [play_again_button, main_menu_button]
        choice = self._wait_for_choice(self.player, choices)

        if play_again_button == choice:
            self._transition_to_scene("MainGameScene")
        else:
            self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append(choice.thing)

    def bot_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        self.skill_queue.append(choice.thing)

    def resolution_phase(self):
        player_skill = self.skill_queue.pop(0)
        bot_skill = self.skill_queue.pop(0)

        self._show_text(self.player, f"Your {self.player_creature.display_name} uses {player_skill.display_name}!")
        self.bot_creature.hp = max(0, self.bot_creature.hp - player_skill.damage)
        
        self._show_text(self.player, f"Foe {self.bot_creature.display_name} uses {bot_skill.display_name}!")
        self.player_creature.hp = max(0, self.player_creature.hp - bot_skill.damage)

        # Ensure the skill queue is empty after resolution
        assert len(self.skill_queue) == 0, "Skill queue should be empty after resolution"

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self.skill_queue.clear()
