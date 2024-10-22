from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

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
        while True:
            player_skill = self._player_choice_phase()
            opponent_skill = self._foe_choice_phase()
            self._resolution_phase(player_skill, opponent_skill)
            
            if self._check_battle_end():
                self._transition_to_scene("MainMenuScene")
                break

    def _player_choice_phase(self):
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _foe_choice_phase(self):
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)") for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, opponent_skill):
        first, second = self._determine_order(self.player_creature, self.opponent_creature, player_skill, opponent_skill)
        self._execute_skill(*first)
        if not self._check_battle_end():
            self._execute_skill(*second)

    def _determine_order(self, player_creature, opponent_creature, player_skill, opponent_skill):
        if player_creature.speed > opponent_creature.speed:
            return (self.player, player_creature, opponent_creature, player_skill), (self.opponent, opponent_creature, player_creature, opponent_skill)
        elif player_creature.speed < opponent_creature.speed:
            return (self.opponent, opponent_creature, player_creature, opponent_skill), (self.player, player_creature, opponent_creature, player_skill)
        else:
            if random.random() < 0.5:
                return (self.player, player_creature, opponent_creature, player_skill), (self.opponent, opponent_creature, player_creature, opponent_skill)
            else:
                return (self.opponent, opponent_creature, player_creature, opponent_skill), (self.player, player_creature, opponent_creature, player_skill)

    def _execute_skill(self, attacker, attacker_creature, defender_creature, skill):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        factor = self._get_weakness_resistance_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender_creature.display_name}!")

    def _get_weakness_resistance_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False
