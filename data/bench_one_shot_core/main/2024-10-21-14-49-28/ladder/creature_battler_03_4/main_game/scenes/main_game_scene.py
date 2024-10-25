from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        while not self.battle_ended:
            player_action = self._player_choice_phase()
            opponent_action = self._opponent_choice_phase()
            self._resolution_phase([player_action, opponent_action])
        
        self._end_battle()

    def _player_choice_phase(self):
        self._show_text(self.player, "Your turn!")
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.skill_type} type)") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return (self.player_creature, choice.thing)

    def _opponent_choice_phase(self):
        self._show_text(self.player, f"{self.opponent.display_name}'s turn!")
        skill = random.choice(self.opponent_creature.skills)
        return (self.opponent_creature, skill)

    def _resolution_phase(self, actions):
        # Sort actions based on creature speed, with random tiebreaker
        sorted_actions = sorted(actions, key=lambda x: (x[0].speed, random.random()), reverse=True)
        
        for attacker, skill in sorted_actions:
            if attacker == self.player_creature:
                defender = self.opponent_creature
            else:
                defender = self.player_creature
            
            self._execute_skill(attacker, defender, skill)
            if self._check_battle_end():
                break

    def _execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name}!")
        raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{defender.display_name} takes {final_damage} damage!")

    def _get_type_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire" and defender_type == "leaf":
            return 2.0
        elif skill_type == "water" and defender_type == "fire":
            return 2.0
        elif skill_type == "leaf" and defender_type == "water":
            return 2.0
        elif skill_type == "fire" and defender_type == "water":
            return 0.5
        elif skill_type == "water" and defender_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and defender_type == "fire":
            return 0.5
        else:
            return 1.0

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            self.battle_ended = True
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
            self.battle_ended = True
            return True
        return False

    def _end_battle(self):
        self._show_text(self.player, "The battle has ended!")
        self._show_text(self.player, "Returning to the main menu...")
        self._transition_to_scene("MainMenuScene")
