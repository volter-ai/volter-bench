from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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

Your skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}

Foe's skills:
{', '.join([skill.display_name for skill in self.foe_creature.skills])}

Skill Queue:
{', '.join([skill.display_name for skill in self.skill_queue])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appears!")
        
        while True:
            # Player Choice Phase
            self.player_choice_phase()
            
            # Foe Choice Phase
            self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase()
            
            # Check for battle end
            if self.check_battle_end():
                break

        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append(choice.thing)
        self._show_text(self.player, f"You chose {choice.thing.display_name}!")

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.skill_queue.append(choice.thing)
        self._show_text(self.player, f"Foe chose {choice.thing.display_name}!")

    def resolution_phase(self):
        while self.skill_queue:
            skill = self.skill_queue.pop(0)
            if skill in self.player_creature.skills:
                self._show_text(self.player, f"You used {skill.display_name}!")
                self.foe_creature.hp -= skill.damage
                self._show_text(self.player, f"Foe {self.foe_creature.display_name} took {skill.damage} damage!")
            else:
                self._show_text(self.player, f"Foe {self.foe_creature.display_name} used {skill.display_name}!")
                self.player_creature.hp -= skill.damage
                self._show_text(self.player, f"Your {self.player_creature.display_name} took {skill.damage} damage!")

            if self.check_battle_end():
                break

    def check_battle_end(self):
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, f"Foe {self.foe_creature.display_name} fainted! You win!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            return True
        return False

    def reset_creatures_state(self):
        for creature in self.player.creatures + self.foe.creatures:
            creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
