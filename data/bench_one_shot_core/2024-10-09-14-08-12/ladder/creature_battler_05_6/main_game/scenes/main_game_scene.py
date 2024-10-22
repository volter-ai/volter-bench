import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.player_action = None
        self.bot_action = None

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name}:
HP: {player_creature.hp}/{player_creature.max_hp}

{self.bot.display_name}'s {bot_creature.display_name}:
HP: {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
> Back
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.turn_counter += 1
            self._player_turn()
            if self.player_action is None:
                continue  # Player chose to go back, restart the turn
            self._bot_turn()
            self._resolve_turn()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            choices = [attack_button, swap_button, back_button]
            choice = self._wait_for_choice(self.player, choices)

            if back_button == choice:
                self.player_action = None
                return

            if attack_button == choice:
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                
                if isinstance(skill_choice, Button) and skill_choice.display_name == "Back":
                    continue  # Go back to the main choice
                
                self.player_action = ("attack", skill_choice.thing)
                break
            elif swap_button == choice:
                creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
                if creature_choices:
                    creature_choices.append(Button("Back"))
                    creature_choice = self._wait_for_choice(self.player, creature_choices)
                    
                    if isinstance(creature_choice, Button) and creature_choice.display_name == "Back":
                        continue  # Go back to the main choice
                    
                    self.player_action = ("swap", creature_choice.thing)
                    break
                else:
                    self._show_text(self.player, "No other creatures available to swap!")

    def _bot_turn(self):
        bot_creature = self.bot.active_creature
        
        # Decide whether to attack or swap
        if random.random() < 0.2 and len([c for c in self.bot.creatures if c != bot_creature and c.hp > 0]) > 0:
            # Swap
            swap_creatures = [c for c in self.bot.creatures if c != bot_creature and c.hp > 0]
            new_creature = random.choice(swap_creatures)
            self.bot_action = ("swap", new_creature)
        else:
            # Attack
            skill = random.choice(bot_creature.skills)
            self.bot_action = ("attack", skill)
        
        # Simulate bot's choice for consistency with player's turn
        action_type, action_data = self.bot_action
        if action_type == "attack":
            self._wait_for_choice(self.bot, [SelectThing(action_data)])
        elif action_type == "swap":
            self._wait_for_choice(self.bot, [SelectThing(action_data)])

    def _resolve_turn(self):
        first, second = self._determine_turn_order()
        self._execute_action(*first)
        if self._check_battle_end():
            return
        self._execute_action(*second)

    def _determine_turn_order(self):
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        if self.player_action[0] == "swap" or self.bot_action[0] == "swap":
            return (self.player, self.player_action), (self.bot, self.bot_action)
        elif player_speed > bot_speed or (player_speed == bot_speed and random.random() < 0.5):
            return (self.player, self.player_action), (self.bot, self.bot_action)
        else:
            return (self.bot, self.bot_action), (self.player, self.player_action)

    def _execute_action(self, actor, action):
        action_type, action_data = action
        if action_type == "attack":
            self._execute_attack(actor, action_data)
        elif action_type == "swap":
            self._execute_swap(actor, action_data)

    def _execute_attack(self, attacker, skill):
        if attacker == self.player:
            defender = self.bot
        else:
            defender = self.player
        
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.active_creature.display_name} took {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self._force_swap(defender)

    def _execute_swap(self, player, new_creature):
        old_creature = player.active_creature
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped {old_creature.display_name} for {new_creature.display_name}!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        else:
            raw_damage = (float(attacker.sp_attack) / float(defender.sp_defense)) * float(skill.base_damage)
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if player == self.player:
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                choice = self._wait_for_choice(player, creature_choices)
                new_creature = choice.thing
            else:
                new_creature = random.choice(available_creatures)
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures left!")

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        # Only reset the player's creatures, not the bot's
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
