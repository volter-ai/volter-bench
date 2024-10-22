from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
from typing import Tuple
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.foe.active_creature = self.foe.creatures[0]
        self.turn_actions = []

    def __str__(self):
        player_creature = self.player.active_creature
        foe_creature = self.foe.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.foe.display_name}'s {foe_creature.display_name}: HP {foe_creature.hp}/{foe_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices + [Button("Back")])
                if isinstance(skill_choice, SelectThing):
                    self.turn_actions.append(("player", "attack", skill_choice.thing))
                    break
            elif choice == swap_button:
                creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
                creature_choice = self._wait_for_choice(self.player, creature_choices + [Button("Back")])
                if isinstance(creature_choice, SelectThing):
                    self.turn_actions.append(("player", "swap", creature_choice.thing))
                    break

    def foe_choice_phase(self):
        available_creatures = [creature for creature in self.foe.creatures if creature != self.foe.active_creature and creature.hp > 0]
        
        choices = []
        if self.foe.active_creature.skills:
            choices.append(Button("Attack"))
        if available_creatures:
            choices.append(Button("Swap"))
        
        if not choices:
            self._show_text(self.player, f"{self.foe.display_name} has no available actions!")
            return

        foe_choice = self._wait_for_choice(self.foe, choices)
        
        if foe_choice.display_name == "Attack":
            skill_choice = self._wait_for_choice(self.foe, [SelectThing(skill) for skill in self.foe.active_creature.skills])
            self.turn_actions.append(("foe", "attack", skill_choice.thing))
        elif foe_choice.display_name == "Swap":
            creature_choice = self._wait_for_choice(self.foe, [SelectThing(creature) for creature in available_creatures])
            self.turn_actions.append(("foe", "swap", creature_choice.thing))

    def get_action_priority(self, action: Tuple[str, str, Skill or Creature]) -> Tuple[int, float]:
        player, action_type, target = action
        if action_type == "swap":
            return (float('inf'), random.random())  # Swaps always go first
        else:
            if player == "player":
                speed = self.player.active_creature.speed
            else:
                speed = self.foe.active_creature.speed
            return (speed, random.random())  # Use random as a tiebreaker

    def resolution_phase(self):
        # Sort actions based on speed and randomness for tiebreaking
        sorted_actions = sorted(self.turn_actions, key=self.get_action_priority, reverse=True)

        for action in sorted_actions:
            player, action_type, target = action
            if action_type == "swap":
                if player == "player":
                    self.player.active_creature = target
                else:
                    self.foe.active_creature = target
                self._show_text(self.player, f"{player.capitalize()} swapped to {target.display_name}!")
            else:
                self.execute_attack(player, target)
        
        self.turn_actions.clear()

    def execute_attack(self, attacker: str, skill: Skill):
        if attacker == "player":
            attacking_creature = self.player.active_creature
            defending_creature = self.foe.active_creature
        else:
            attacking_creature = self.foe.active_creature
            defending_creature = self.player.active_creature

        damage = self.calculate_damage(attacking_creature, defending_creature, skill)
        defending_creature.hp = max(0, defending_creature.hp - damage)

        self._show_text(self.player, f"{attacking_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defending_creature.display_name} took {damage} damage!")

        if defending_creature.hp == 0:
            self._show_text(self.player, f"{defending_creature.display_name} fainted!")
            self.handle_fainted_creature(attacker)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

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

    def handle_fainted_creature(self, last_attacker: str):
        if last_attacker == "player":
            player = self.foe
        else:
            player = self.player

        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self.end_battle(last_attacker)

    def check_battle_end(self) -> bool:
        if all(creature.hp == 0 for creature in self.player.creatures):
            self.end_battle("foe")
            return True
        elif all(creature.hp == 0 for creature in self.foe.creatures):
            self.end_battle("player")
            return True
        return False

    def end_battle(self, winner: str):
        if winner == "player":
            self._show_text(self.player, "Congratulations! You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle. Better luck next time!")
        
        # Reset creature HP
        for creature in self.player.creatures + self.foe.creatures:
            creature.hp = creature.max_hp

        self._transition_to_scene("MainMenuScene")
