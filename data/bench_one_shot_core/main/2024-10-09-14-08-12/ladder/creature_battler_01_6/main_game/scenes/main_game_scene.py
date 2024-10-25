from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
from typing import List, Tuple


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[Tuple[Creature, Skill]] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}

Skill Queue:
{', '.join(f"{creature.display_name}'s {skill.display_name}" for creature, skill in self.skill_queue)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        
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

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append((self.player_creature, choice.thing))

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.skill_queue.append((self.foe_creature, choice.thing))

    def resolution_phase(self):
        while self.skill_queue:
            creature, skill = self.skill_queue.pop(0)
            if creature == self.player_creature:
                target = self.foe_creature
                self._show_text(self.player, f"Your {creature.display_name} used {skill.display_name}!")
            else:
                target = self.player_creature
                self._show_text(self.player, f"Foe's {creature.display_name} used {skill.display_name}!")
            
            target.hp = max(0, target.hp - skill.damage)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.foe_creature.hp == 0:
            self._show_text(self.player, f"Foe's {self.foe_creature.display_name} fainted! You won the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
        self.skill_queue.clear()
