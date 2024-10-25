from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
from typing import Tuple
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_counter = 0

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Main Game===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name}:
HP: {player_creature.hp}/{player_creature.max_hp}

{self.opponent.display_name}'s {opponent_creature.display_name}:
HP: {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.turn_counter += 1
            player_action = self._player_choice_phase(self.player)
            opponent_action = self._player_choice_phase(self.opponent)
            self._resolution_phase(player_action, opponent_action)
            
            if self._check_battle_end():
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_choice_phase(self, player: Player) -> Tuple[str, Skill | Creature]:
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                skill = self._choose_skill(player)
                if skill:
                    return "attack", skill
            elif swap_button == choice:
                creature = self._choose_creature(player)
                if creature:
                    return "swap", creature

    def _choose_skill(self, player: Player) -> Skill | None:
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills] + [back_button]
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return choice.thing

    def _choose_creature(self, player: Player) -> Creature | None:
        back_button = Button("Back")
        choices = [SelectThing(creature) for creature in player.creatures 
                   if creature != player.active_creature and creature.hp > 0] + [back_button]
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return choice.thing

    def _resolution_phase(self, player_action: Tuple[str, Skill | Creature], 
                          opponent_action: Tuple[str, Skill | Creature]):
        actions = [
            ("player", *player_action),
            ("opponent", *opponent_action)
        ]
        
        # Sort actions: swaps first, then by creature speed with random tie-breaking
        actions.sort(key=lambda x: (
            0 if x[1] == "swap" else 1,
            -self._get_creature_speed(x[0]),
            random.random()  # Random tie-breaker
        ))

        for action in actions:
            if action[1] == "swap":
                self._perform_swap(action[0], action[2])
            else:
                self._perform_attack(action[0], action[2])

    def _get_creature_speed(self, actor: str) -> int:
        if actor == "player":
            return self.player.active_creature.speed
        else:
            return self.opponent.active_creature.speed

    def _perform_swap(self, actor: str, creature: Creature):
        if actor == "player":
            self.player.active_creature = creature
            self._show_text(self.player, f"{self.player.display_name} swapped to {creature.display_name}!")
        else:
            self.opponent.active_creature = creature
            self._show_text(self.player, f"{self.opponent.display_name} swapped to {creature.display_name}!")

    def _perform_attack(self, actor: str, skill: Skill):
        if actor == "player":
            attacker, defender = self.player.active_creature, self.opponent.active_creature
            attacker_name, defender_name = self.player.display_name, self.opponent.display_name
        else:
            attacker, defender = self.opponent.active_creature, self.player.active_creature
            attacker_name, defender_name = self.opponent.display_name, self.player.display_name

        damage = self._calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)

        self._show_text(self.player, f"{attacker_name}'s {attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_name}'s {defender.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type:
            return 1.0
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2.0
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0.5
        else:
            return 1.0

    def _check_battle_end(self) -> bool:
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, f"{self.player.display_name} has lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, f"{self.player.display_name} has won the battle!")
            return True
        
        if self.player.active_creature.hp == 0:
            self._force_swap(self.player)
        if self.opponent.active_creature.hp == 0:
            self._force_swap(self.opponent)
        
        return False

    def _force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(self.player, f"{player.display_name} swapped to {player.active_creature.display_name}!")

    def _reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
