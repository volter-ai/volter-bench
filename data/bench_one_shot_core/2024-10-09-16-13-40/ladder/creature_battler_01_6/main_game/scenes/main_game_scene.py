from collections import deque

from main_game.models import Creature
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue = deque()

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            self.player_choice_phase()
            
            # Foe Choice Phase
            self.foe_choice_phase()
            
            # Resolution Phase
            if self.resolution_phase():
                break

        # Reset creatures before transitioning out of the scene
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def show_skills(self, creature: Creature):
        skill_list = ", ".join([f"{skill.display_name} (Damage: {skill.damage})" for skill in creature.skills])
        return f"{creature.display_name}'s skills: {skill_list}"

    def is_knocked_out(self, creature: Creature) -> bool:
        return creature.hp <= 0

    def player_choice_phase(self):
        self._show_text(self.player, self.show_skills(self.player_creature))
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append((self.player, choice.thing))

    def foe_choice_phase(self):
        self._show_text(self.foe, self.show_skills(self.foe_creature))
        choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.skill_queue.append((self.foe, choice.thing))

    def resolution_phase(self) -> bool:
        while self.skill_queue:
            acting_player, skill = self.skill_queue.popleft()
            if acting_player == self.player:
                self._show_text(self.player, f"You used {skill.display_name}!")
                self.foe_creature.hp -= skill.damage
                self._show_text(self.player, f"Foe {self.foe_creature.display_name} took {skill.damage} damage!")
                if self.is_knocked_out(self.foe_creature):
                    self._show_text(self.player, f"Foe {self.foe_creature.display_name} fainted! You win!")
                    return True
            else:
                self._show_text(self.player, f"Foe {self.foe_creature.display_name} used {skill.display_name}!")
                self.player_creature.hp -= skill.damage
                self._show_text(self.player, f"Your {self.player_creature.display_name} took {skill.damage} damage!")
                if self.is_knocked_out(self.player_creature):
                    self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
                    return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.foe.creatures:
            creature.hp = creature.max_hp
