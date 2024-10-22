import random
from dataclasses import dataclass
from typing import Union

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


@dataclass
class Action:
    player: Player
    action_type: str
    target: Union[Skill, Creature]

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.action_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===

{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.action_queue = []
            
            player_action = self._player_choice_phase(self.player)
            bot_action = self._player_choice_phase(self.bot)
            
            self.action_queue.append(player_action)
            self.action_queue.append(bot_action)
            
            self._resolution_phase()
            
            if self._check_battle_end():
                break

        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        self._show_text(self.player, f"{self.player.display_name} sends out {self.player.active_creature.display_name}!")
        self._show_text(self.bot, f"{self.bot.display_name} sends out {self.bot.active_creature.display_name}!")

    def _player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            
            choices = [attack_button, swap_button, back_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                if skill_choice == back_button:
                    continue
                return Action(current_player, "attack", skill_choice.thing)
            elif choice == swap_button:
                available_creatures = [creature for creature in current_player.creatures 
                                       if creature != current_player.active_creature and creature.hp > 0]
                if not available_creatures:
                    self._show_text(current_player, "No creatures available to swap!")
                    continue
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(back_button)
                creature_choice = self._wait_for_choice(current_player, creature_choices)
                if creature_choice == back_button:
                    continue
                return Action(current_player, "swap", creature_choice.thing)
            elif choice == back_button:
                continue

    def _resolution_phase(self):
        self.action_queue.sort(key=lambda x: x.player.active_creature.speed, reverse=True)
        
        # Handle equal speed scenario
        # Note: This is not explicitly described in the architecture, but it's a reasonable approach
        if len(self.action_queue) == 2 and self.action_queue[0].player.active_creature.speed == self.action_queue[1].player.active_creature.speed:
            random.shuffle(self.action_queue)

        for action in self.action_queue:
            if action.action_type == "swap":
                self._perform_swap(action.player, action.target)
            elif action.action_type == "attack":
                self._perform_attack(action.player, action.target)
            
            # Check if forced swap is needed after each action
            self._check_forced_swap(self.player)
            self._check_forced_swap(self.bot)

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)  # Explicitly convert to integer
        return max(1, final_damage)

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 1, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 1, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 1}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_forced_swap(self, player):
        if player.active_creature.hp == 0:
            available_creatures = [creature for creature in player.creatures if creature.hp > 0]
            if available_creatures:
                self._show_text(player, f"{player.active_creature.display_name} has fainted!")
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choice = self._wait_for_choice(player, creature_choices)
                self._perform_swap(player, creature_choice.thing)
            else:
                self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def _check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                return True
        return False

    def _end_battle(self):
        # Reset the state of the player's creatures only
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        self.player.active_creature = None  # Reset active creature

        self._show_text(self.player, "The battle has ended. Returning to the main menu.")
        self._transition_to_scene("MainMenuScene")
