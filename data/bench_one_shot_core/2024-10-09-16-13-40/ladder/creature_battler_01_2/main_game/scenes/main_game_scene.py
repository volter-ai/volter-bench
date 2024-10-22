from typing import List

from main_game.models import Creature, Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp} {'(Knocked Out)' if self.player_creature.knocked_out else ''}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp} {'(Knocked Out)' if self.foe_creature.knocked_out else ''}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player Choice Phase
            self.player_turn()
            
            # Foe Choice Phase
            self.foe_turn()
            
            # Resolution Phase
            self.resolve_turn()
            
            # Check for battle end
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        if not self.player_creature.knocked_out:
            choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, choices)
            self.skill_queue.append(choice.thing)
        else:
            self._show_text(self.player, f"Your {self.player_creature.display_name} is knocked out and cannot act!")

    def foe_turn(self):
        if not self.foe_creature.knocked_out:
            choices = [SelectThing(skill, label=skill.display_name) for skill in self.foe_creature.skills]
            choice = self._wait_for_choice(self.foe, choices)
            self.skill_queue.append(choice.thing)
        else:
            self._show_text(self.foe, f"Your {self.foe_creature.display_name} is knocked out and cannot act!")

    def resolve_turn(self):
        while self.skill_queue:
            skill = self.skill_queue.pop(0)
            if skill in self.player_creature.skills and not self.player_creature.knocked_out:
                self.foe_creature.hp -= skill.damage
                self._show_text(self.player, f"Your {self.player_creature.display_name} used {skill.display_name}!")
                self._show_text(self.foe, f"Opponent's {self.player_creature.display_name} used {skill.display_name}!")
                self.check_knocked_out(self.foe_creature)
            elif not self.foe_creature.knocked_out:
                self.player_creature.hp -= skill.damage
                self._show_text(self.player, f"Foe's {self.foe_creature.display_name} used {skill.display_name}!")
                self._show_text(self.foe, f"Your {self.foe_creature.display_name} used {skill.display_name}!")
                self.check_knocked_out(self.player_creature)

    def check_knocked_out(self, creature: Creature):
        if creature.hp <= 0:
            creature.hp = 0
            creature.knocked_out = True
            self._show_text(self.player, f"{creature.display_name} has been knocked out!")
            self._show_text(self.foe, f"{creature.display_name} has been knocked out!")

    def check_battle_end(self):
        if self.player_creature.knocked_out and self.foe_creature.knocked_out:
            self._show_text(self.player, "The battle ended in a draw!")
            self._show_text(self.foe, "The battle ended in a draw!")
            return True
        elif self.player_creature.knocked_out:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            return True
        elif self.foe_creature.knocked_out:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.player_creature.knocked_out = False
        self.foe_creature.hp = self.foe_creature.max_hp
        self.foe_creature.knocked_out = False
