from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Skill
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Available skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}

Skill Queue: {', '.join(skill.display_name for skill in self.skill_queue)}
"""

    def run(self):
        while True:
            self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
            
            while True:
                # Clear the skill queue at the start of each turn
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

            # Ask player if they want to play again or return to main menu
            play_again_button = Button("Play Again")
            main_menu_button = Button("Return to Main Menu")
            choices = [play_again_button, main_menu_button]
            choice = self._wait_for_choice(self.player, choices)

            if main_menu_button == choice:
                self._transition_to_scene("MainMenuScene")
                return
            elif play_again_button == choice:
                # Reset the battle for a new round
                self.foe = self._app.create_bot("default_player")
                self.player_creature = self.player.creatures[0]
                self.foe_creature = self.foe.creatures[0]
                continue

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append(choice.thing)

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.skill_queue.append(choice.thing)

    def resolution_phase(self):
        for skill in self.skill_queue:
            if skill in self.player_creature.skills:
                self._show_text(self.player, f"{self.player_creature.display_name} used {skill.display_name}!")
                self.foe_creature.hp -= skill.damage
            else:
                self._show_text(self.player, f"{self.foe_creature.display_name} used {skill.display_name}!")
                self.player_creature.hp -= skill.damage

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.foe.creatures:
            creature.hp = creature.max_hp
