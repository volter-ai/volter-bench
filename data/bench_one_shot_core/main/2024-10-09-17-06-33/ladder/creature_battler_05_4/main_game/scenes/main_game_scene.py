from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Main Game===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

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
            self._player_turn(self.player)
            self._player_turn(self.bot)
            self._resolve_turn()
            
            if self._check_battle_end():
                break

        self._end_battle()

    def _player_turn(self, player):
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
        skills = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices = skills + [back_button]
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return choice.thing

    def _choose_swap_creature(self, player):
        available_creatures = [creature for creature in player.creatures 
                               if creature != player.active_creature and creature.hp > 0]
        creatures = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creatures + [back_button]
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return choice.thing

    def _resolve_turn(self):
        # Sort the turn queue, with swaps always going first
        self.turn_queue.sort(key=lambda x: x[1] != "swap")
        
        # For actions with equal priority (i.e., both attacks), randomly choose the order
        attack_actions = [action for action in self.turn_queue if action[1] == "attack"]
        if len(attack_actions) == 2:
            random.shuffle(attack_actions)
            self.turn_queue = [action for action in self.turn_queue if action[1] == "swap"] + attack_actions
        
        for player, action, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                self._execute_skill(player, target)
        
        self.turn_queue.clear()

    def _execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature
        
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)  # Explicitly convert to integer
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")
        
        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} fainted!")
            self._force_swap(defender)

    def _get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, creature_type), 1)

    def _force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return
        
        creatures = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creatures)
        player.active_creature = choice.thing
        self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def _check_battle_end(self):
        player_creatures_alive = any(creature.hp > 0 for creature in self.player.creatures)
        bot_creatures_alive = any(creature.hp > 0 for creature in self.bot.creatures)
        
        if not player_creatures_alive:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_creatures_alive:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        # Only reset the player's creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
