from typing import List

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.battle_count = 0
        self.max_battles = 3
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
        while self.battle_count < self.max_battles:
            self._show_text(self.player, f"Battle {self.battle_count + 1} of {self.max_battles}")
            self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
            
            while True:
                self.skill_queue.clear()
                
                # Player Choice Phase
                self._player_choice_phase()
                
                # Foe Choice Phase
                self._foe_choice_phase()
                
                # Resolution Phase
                self._resolution_phase()
                
                # Check for battle end
                if self._check_battle_end():
                    break

            self._reset_creatures()
            self.battle_count += 1

            if self.battle_count < self.max_battles:
                continue_button = Button("Continue to next battle")
                quit_button = Button("Quit game")
                choice = self._wait_for_choice(self.player, [continue_button, quit_button])
                if choice == quit_button:
                    self._quit_whole_game()
                    return
            else:
                self._show_text(self.player, "You've completed all battles!")

        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append(choice.thing)

    def _foe_choice_phase(self):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.skill_queue.append(choice.thing)

    def _resolution_phase(self):
        for skill in self.skill_queue:
            if skill in self.player_creature.skills:
                self._resolve_skill(self.player, self.player_creature, self.foe_creature, skill)
            else:
                self._resolve_skill(self.foe, self.foe_creature, self.player_creature, skill)
            self.skill_queue.remove(skill)

    def _resolve_skill(self, attacker: Player, attacker_creature: Creature, defender_creature: Creature, skill: Skill):
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        defender_creature.hp -= skill.damage
        self._show_text(self.player, f"{defender_creature.display_name} took {skill.damage} damage!")

    def _check_battle_end(self):
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, f"Foe {self.foe_creature.display_name} fainted! You win!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
