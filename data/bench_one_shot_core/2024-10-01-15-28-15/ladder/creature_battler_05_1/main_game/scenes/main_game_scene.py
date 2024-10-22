import random

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.initialize_battle()
        self.turn_count = 0

    def initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""
Player: {self.player.display_name}
Active Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})

Opponent: {self.opponent.display_name}
Active Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})

1. Attack
2. Swap
"""

    def run(self):
        self._show_text(self.player, str(self))
        self.player_turn()
        if self.check_battle_end():
            return True
        self.opponent_turn()
        if self.check_battle_end():
            return True
        self.turn_count += 1
        return False

    def player_turn(self):
        choices = [Button("Attack"), Button("Swap")]
        choice = self._wait_for_choice(self.player, choices)
        if choice.display_name == "Attack":
            self.handle_attack(self.player)
        elif choice.display_name == "Swap":
            if not self.can_swap(self.player):
                self._show_text(self.player, "No creatures available to swap!")
            else:
                self.handle_swap(self.player)

    def opponent_turn(self):
        if random.choice([True, False]) and self.can_swap(self.opponent):
            self.handle_swap(self.opponent)
        else:
            self.handle_attack(self.opponent)

    def handle_attack(self, attacker: Player):
        skills = attacker.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        skill_choice = self._wait_for_choice(attacker, skill_choices)
        self.execute_skill(attacker, skill_choice.thing)

    def can_swap(self, player: Player) -> bool:
        return any(c.hp > 0 and c != player.active_creature for c in player.creatures)

    def handle_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(player, f"{player.display_name} has no creatures available to swap!")
            return
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        creature_choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = creature_choice.thing
        self._show_text(player, f"{player.display_name} swapped to {player.active_creature.display_name}!")

    def execute_skill(self, attacker: Player, skill: Skill):
        defender = self.opponent if attacker == self.player else self.player
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def check_battle_end(self) -> bool:
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
