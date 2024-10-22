from dataclasses import dataclass
from typing import Union

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


@dataclass
class Action:
    player: Player
    action_type: str
    thing: Union[Skill, Creature]

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        if self.player.creatures:
            self.player.active_creature = self.player.creatures[0]
        if self.bot.creatures:
            self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
{self.player.display_name}: {player_creature.display_name if player_creature else 'No active creature'} (HP: {player_creature.hp}/{player_creature.max_hp} if player_creature else 'N/A')
{self.bot.display_name}: {bot_creature.display_name if bot_creature else 'No active creature'} (HP: {bot_creature.hp}/{bot_creature.max_hp} if bot_creature else 'N/A')

> Attack
> Swap
"""

    def run(self):
        while True:
            actions = []
            actions.append(self.player_turn())
            if self.check_battle_end():
                break
            actions.append(self.bot_turn())
            if self.check_battle_end():
                break
            self.resolve_actions(actions)
            if self.check_battle_end():
                break
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        return self.get_player_action(self.player)

    def bot_turn(self):
        self._show_text(self.player, f"It's {self.bot.display_name}'s turn!")
        return self.get_player_action(self.bot)

    def get_player_action(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                action = self.choose_skill(current_player)
            elif choice == swap_button:
                action = self.choose_swap(current_player)

            if action:
                return action

    def choose_skill(self, current_player):
        if current_player.active_creature:
            skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
            back_button = Button("Back")
            skill_choices.append(back_button)
            choice = self._wait_for_choice(current_player, skill_choices)
            if choice == back_button:
                return None
            return Action(current_player, "attack", choice.thing)
        return None

    def choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
        if not available_creatures:
            self._show_text(current_player, "No creatures available to swap.")
            return None
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        creature_choices.append(back_button)
        choice = self._wait_for_choice(current_player, creature_choices)
        if choice == back_button:
            return None
        return Action(current_player, "swap", choice.thing)

    def resolve_actions(self, actions):
        # Sort actions based on speed (swap actions first, then by creature speed)
        # Use the original order as a tie-breaker for equal speeds
        sorted_actions = sorted(enumerate(actions), key=lambda x: (
            x[1].action_type != "swap",
            -x[1].player.active_creature.speed,
            x[0]  # Use the original index as a tie-breaker
        ))
        
        for _, action in sorted_actions:
            if action.action_type == "attack":
                self.execute_skill(action.player, self.get_opponent(action.player), action.thing)
            elif action.action_type == "swap":
                self.swap_creature(action.player, action.thing)
                # If the opponent used an attack, it hits the swapped-in creature
                opponent_action = next((a for _, a in sorted_actions if a.player != action.player), None)
                if opponent_action and opponent_action.action_type == "attack":
                    self.execute_skill(opponent_action.player, action.player, opponent_action.thing)

    def get_opponent(self, player):
        return self.bot if player == self.player else self.player

    def execute_skill(self, attacker, defender, skill):
        if attacker.active_creature and defender.active_creature:
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")
            if defender.active_creature.hp == 0:
                self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
                self.force_swap(defender)

    def swap_creature(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        else:
            raw_damage = (float(attacker.sp_attack) / float(defender.sp_defense)) * float(skill.base_damage)

        type_factor = float(self.get_type_factor(skill.skill_type, defender.creature_type))
        final_damage = type_factor * raw_damage
        return max(1, int(final_damage))  # Truncate to integer and ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "normal": {"normal": 1.0, "fire": 1.0, "water": 1.0, "leaf": 1.0},
            "fire": {"normal": 1.0, "fire": 0.5, "water": 0.5, "leaf": 2.0},
            "water": {"normal": 1.0, "fire": 2.0, "water": 0.5, "leaf": 0.5},
            "leaf": {"normal": 1.0, "fire": 0.5, "water": 2.0, "leaf": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, f"All your creatures have fainted. You lost the battle!")
            self._show_text(self.player, f"Game Over. Returning to the main menu.")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, f"All opponent's creatures have fainted. You won the battle!")
            self._show_text(self.player, f"Congratulations! Returning to the main menu.")
            return True
        return False

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            self._show_text(self.player, f"{player.display_name} has no more creatures able to battle!")
            return False
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, creature_choices)
        self.swap_creature(player, new_creature.thing)
        return True
