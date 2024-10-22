from typing import List

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.battle_ended = False
        self.skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        
        while not self.battle_ended:
            # Player Choice Phase
            self._player_choice_phase()
            
            # Foe Choice Phase
            self._foe_choice_phase()
            
            # Resolution Phase
            self._resolution_phase()
            
            # Check for battle end
            self._check_battle_end()

        # Transition back to the main menu after the battle ends
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        choices = [SelectThing(skill, label=f"{skill.display_name} (Damage: {skill.damage})") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append(choice.thing)

    def _foe_choice_phase(self):
        choices = [SelectThing(skill, label=f"{skill.display_name} (Damage: {skill.damage})") for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.skill_queue.append(choice.thing)

    def _resolution_phase(self):
        while self.skill_queue:
            skill = self.skill_queue[0]
            if skill in self.player_creature.skills:
                self._execute_skill(self.player, self.player_creature, self.foe_creature, skill)
            else:
                self._execute_skill(self.foe, self.foe_creature, self.player_creature, skill)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, defender_creature: Creature, skill: Skill):
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        defender_creature.hp -= skill.damage
        self._show_text(self.player, f"{defender_creature.display_name} took {skill.damage} damage!")
        self.skill_queue.pop(0)  # Remove the executed skill from the queue

    def _check_battle_end(self):
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, f"Foe's {self.foe_creature.display_name} fainted! You win!")
            self._reset_creatures()
            self.battle_ended = True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            self._reset_creatures()
            self.battle_ended = True

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
        self.skill_queue.clear()  # Clear the skill queue when resetting
