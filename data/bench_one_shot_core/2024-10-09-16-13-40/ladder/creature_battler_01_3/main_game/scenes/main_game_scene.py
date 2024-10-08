from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Skill
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.player_skill_queue: List[Skill] = []
        self.foe_skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}

Queued skills:
Player: {', '.join(skill.display_name for skill in self.player_skill_queue)}
Foe: {', '.join(skill.display_name for skill in self.foe_skill_queue)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appears!")
        
        while True:
            # Player Choice Phase
            self.player_choice_phase()
            
            # Foe Choice Phase
            self.foe_choice_phase()
            
            # Resolution Phase
            self.execute_skills()
            
            # Check for battle end
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill_queue.append(choice.thing)

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.foe_skill_queue.append(choice.thing)

    def execute_skills(self):
        while self.player_skill_queue or self.foe_skill_queue:
            if self.player_skill_queue:
                player_skill = self.player_skill_queue.pop(0)
                self._show_text(self.player, f"You used {player_skill.display_name}!")
                self.foe_creature.hp -= player_skill.damage
                self._show_text(self.player, f"Foe {self.foe_creature.display_name} took {player_skill.damage} damage!")

            if self.foe_creature.hp > 0 and self.foe_skill_queue:
                foe_skill = self.foe_skill_queue.pop(0)
                self._show_text(self.player, f"Foe {self.foe_creature.display_name} used {foe_skill.display_name}!")
                self.player_creature.hp -= foe_skill.damage
                self._show_text(self.player, f"Your {self.player_creature.display_name} took {foe_skill.damage} damage!")

            if self.check_battle_end():
                break

    def check_battle_end(self) -> bool:
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, f"Foe {self.foe_creature.display_name} fainted! You win!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.foe.creatures:
            creature.hp = creature.max_hp
        self.player_skill_queue.clear()
        self.foe_skill_queue.clear()
