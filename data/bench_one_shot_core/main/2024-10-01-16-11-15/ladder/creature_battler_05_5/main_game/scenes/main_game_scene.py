from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
import time


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.turn_order = []

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
            self._player_turn(self.player)
            if self._check_battle_end():
                break
            self._player_turn(self.bot)
            if self._check_battle_end():
                break
            self._resolve_turn()
        
        time.sleep(2)
        self._reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _player_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                if skill_choice == back_button:
                    continue
                self.turn_order.append((current_player, "attack", skill_choice.thing))
                break
            elif swap_button == choice:
                swap_choices = [SelectThing(creature) for creature in current_player.creatures if creature != current_player.active_creature and creature.hp > 0]
                back_button = Button("Back")
                swap_choices.append(back_button)
                if swap_choices:
                    swap_choice = self._wait_for_choice(current_player, swap_choices)
                    if swap_choice == back_button:
                        continue
                    self.turn_order.append((current_player, "swap", swap_choice.thing))
                    break
                else:
                    self._show_text(current_player, "No other creatures available to swap!")

    def _resolve_turn(self):
        self.turn_order.sort(key=lambda x: (x[0].active_creature.speed + random.random() * 0.1), reverse=True)
        for player, action_type, action in self.turn_order:
            if action_type == "swap":
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped to {action.display_name}!")
            elif action_type == "attack":
                self._execute_skill(player, action)
        self.turn_order.clear()

    def _execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature
        attacker_creature = attacker.active_creature

        if skill.is_physical:
            raw_damage = float(attacker_creature.attack) + float(skill.base_damage) - float(defender_creature.defense)
        else:
            raw_damage = (float(attacker_creature.sp_attack) / float(defender_creature.sp_defense)) * float(skill.base_damage)

        weakness_factor = self._get_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = round(weakness_factor * raw_damage)  # Using round() instead of int()
        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(attacker, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} fainted!")
            self._force_swap(defender)

    def _get_weakness_factor(self, skill_type, defender_type):
        weakness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return weakness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if available_creatures:
            swap_choices = [SelectThing(creature) for creature in available_creatures]
            swap_choice = self._wait_for_choice(player, swap_choices)
            player.active_creature = swap_choice.thing
            self._show_text(player, f"{player.display_name} swapped to {swap_choice.thing.display_name}!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures left!")

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures_state(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
