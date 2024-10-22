import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name if player_creature else 'No active creature'}: HP {player_creature.hp}/{player_creature.max_hp if player_creature else 0}
{self.bot.display_name}'s {bot_creature.display_name if bot_creature else 'No active creature'}: HP {bot_creature.hp}/{bot_creature.max_hp if bot_creature else 0}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        self.game_loop()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def game_loop(self):
        while True:
            self._player_choice_phase(self.player)
            self._player_choice_phase(self.bot)
            self._resolution_phase()

            if self._check_battle_end():
                break

        self._show_battle_result()
        self._exit_scene()

    def _player_choice_phase(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                skill = self._choose_skill(player)
                if skill:
                    self.turn_queue.append((player, "attack", skill))
                    break
            elif swap_button == choice:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    self.turn_queue.append((player, "swap", new_creature))
                    break

    def _choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _resolution_phase(self):
        # Sort the turn queue: swaps first, then by speed (higher speed first), then randomly
        self.turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed, random.random()))
        
        for i, (player, action_type, action) in enumerate(self.turn_queue):
            if action_type == "swap":
                old_creature = player.active_creature
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped {old_creature.display_name} for {action.display_name}!")
                
                # Check if there's a queued attack from the opponent
                opponent = self.bot if player == self.player else self.player
                opponent_action = next((act for act in self.turn_queue[i+1:] if act[0] == opponent and act[1] == "attack"), None)
                
                if opponent_action:
                    self._apply_queued_skill(opponent, opponent_action[2], player)
            elif action_type == "attack":
                self._execute_skill(player, action)

        self.turn_queue.clear()

    def _apply_queued_skill(self, attacker, skill, defender):
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name} on the swapped-in creature!")
        self._execute_skill(attacker, skill, defender.active_creature)

    def _execute_skill(self, attacker, skill, defender_creature=None):
        defender = self.bot if attacker == self.player else self.player
        if defender_creature is None:
            defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = float(attacker.active_creature.attack + skill.base_damage - defender_creature.defense)
        else:
            raw_damage = float(attacker.active_creature.sp_attack) / float(defender_creature.sp_defense) * float(skill.base_damage)

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._handle_knockout(defender)

    def _calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("water", "fire"): 2.0,
            ("leaf", "water"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1.0)

    def _handle_knockout(self, player):
        self._show_text(player, f"{player.display_name}'s {player.active_creature.display_name} was knocked out!")
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def _check_battle_end(self):
        return all(c.hp == 0 for c in self.player.creatures) or all(c.hp == 0 for c in self.bot.creatures)

    def _show_battle_result(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")

    def _reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def _exit_scene(self):
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")
