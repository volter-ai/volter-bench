from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.current_turn = self._determine_turn_order()

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Current Turn: {self.current_turn.capitalize()}

Available Skills:
{self._format_skills(self.player_creature.skills if self.current_turn == "player" else self.opponent_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self.game_loop()

    def game_loop(self):
        while True:
            self._show_text(self.player, str(self))
            
            current_creature = self.player_creature if self.current_turn == "player" else self.opponent_creature
            current_player = self.player if self.current_turn == "player" else self.opponent
            
            choices = [SelectThing(skill) for skill in current_creature.skills]
            choice = self._wait_for_choice(current_player, choices)
            
            skill_used = choice.thing
            self._show_text(self.player, f"{current_creature.display_name} used {skill_used.display_name}!")
            
            target_creature = self.opponent_creature if self.current_turn == "player" else self.player_creature
            damage = self._calculate_damage(skill_used, current_creature, target_creature)
            target_creature.hp = max(0, target_creature.hp - damage)
            
            self._show_text(self.player, f"{target_creature.display_name} took {damage} damage!")
            
            if target_creature.hp == 0:
                winner = self.player if self.current_turn == "player" else self.opponent
                self._show_text(self.player, f"{winner.display_name} wins!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
            
            self.current_turn = self._determine_turn_order()

    def _calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def _determine_turn_order(self) -> str:
        if self.player_creature.speed > self.opponent_creature.speed:
            return "player"
        elif self.opponent_creature.speed > self.player_creature.speed:
            return "opponent"
        else:
            return random.choice(["player", "opponent"])
