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

Your skills:
{self._format_skills(self.player_creature.skills)}

> Use Skill
> Quit
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}: {skill.damage} damage" for skill in skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            self.skill_queue.clear()  # Clear the skill queue at the start of each turn
            
            # Player Choice Phase
            self.player_choice_phase()
            
            # Foe Choice Phase
            self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase()
            
            # Check for battle end
            if self.check_battle_end():
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break

    def player_choice_phase(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if quit_button == choice:
            self._quit_whole_game()

        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        skill_choice = self._wait_for_choice(self.player, skill_choices)
        self.skill_queue.append(skill_choice.thing)

    def foe_choice_phase(self):
        skill_choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        skill_choice = self._wait_for_choice(self.foe, skill_choices)
        self.skill_queue.append(skill_choice.thing)

    def resolution_phase(self):
        for skill in self.skill_queue:
            if skill in self.player_creature.skills:
                self._show_text(self.player, f"You used {skill.display_name}!")
                self.foe_creature.hp -= skill.damage
                self._show_text(self.player, f"Foe's {self.foe_creature.display_name} took {skill.damage} damage!")
            else:
                self._show_text(self.player, f"Foe used {skill.display_name}!")
                self.player_creature.hp -= skill.damage
                self._show_text(self.player, f"Your {self.player_creature.display_name} took {skill.damage} damage!")
            
            if self.check_battle_end():
                break

        self.skill_queue.clear()  # Clear the skill queue after resolution

    def check_battle_end(self):
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.foe.creatures:
            creature.hp = creature.max_hp
