from typing import List

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


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
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        
        battle_ended = False
        while not battle_ended:
            # Player Choice Phase
            player_skill = self._player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self._foe_choice_phase()
            
            # Queue skills
            self._queue_skills(player_skill, foe_skill)
            
            # Resolution Phase
            self._resolution_phase()
            
            # Check for battle end
            battle_ended = self._check_battle_end()

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _foe_choice_phase(self):
        # Show foe's skills to the player
        foe_skills_text = f"Foe's {self.foe_creature.display_name}'s skills:\n{self._format_skills(self.foe_creature.skills)}"
        self._show_text(self.player, foe_skills_text)

        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return choice.thing

    def _queue_skills(self, player_skill: Skill, foe_skill: Skill):
        self.skill_queue = [player_skill, foe_skill]

    def _resolution_phase(self):
        while self.skill_queue:
            skill = self.skill_queue.pop(0)
            if skill in self.player_creature.skills:
                self._execute_skill(self.player, self.player_creature, self.foe_creature, skill)
            else:
                self._execute_skill(self.foe, self.foe_creature, self.player_creature, skill)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, defender_creature: Creature, skill: Skill):
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        defender_creature.hp = max(0, defender_creature.hp - skill.damage)
        self._show_text(self.player, f"{defender_creature.display_name} took {skill.damage} damage!")

    def _check_battle_end(self):
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, f"Foe's {self.foe_creature.display_name} fainted! You win!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
