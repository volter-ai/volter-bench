from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
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
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.opponent, self.opponent_creature)

            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)

            # Check for battle end
            if self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0:
                self._battle_end()
                break

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)") for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        first, second = self._determine_turn_order()
        
        self._execute_skill(first[0], first[1], first[2], second[0], second[1])
        if second[1].hp > 0:
            self._execute_skill(second[0], second[1], second[2], first[0], first[1])

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature, self.player_creature.skills[0]), (self.opponent, self.opponent_creature, self.opponent_creature.skills[0])
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature, self.opponent_creature.skills[0]), (self.player, self.player_creature, self.player_creature.skills[0])
        else:
            if random.choice([True, False]):
                return (self.player, self.player_creature, self.player_creature.skills[0]), (self.opponent, self.opponent_creature, self.opponent_creature.skills[0])
            else:
                return (self.opponent, self.opponent_creature, self.opponent_creature.skills[0]), (self.player, self.player_creature, self.player_creature.skills[0])

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        effectiveness = "It's super effective!" if weakness_factor > 1 else "It's not very effective..." if weakness_factor < 1 else ""
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness}")
        self._show_text(defender, f"{defender_creature.display_name} took {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted. You lost!")
            self._show_text(self.opponent, f"You defeated {self.player.display_name}'s {self.player_creature.display_name}. You won!")
        else:
            self._show_text(self.player, f"You defeated {self.opponent.display_name}'s {self.opponent_creature.display_name}. You won!")
            self._show_text(self.opponent, f"Your {self.opponent_creature.display_name} fainted. You lost!")
        self._transition_to_scene("MainMenuScene")
