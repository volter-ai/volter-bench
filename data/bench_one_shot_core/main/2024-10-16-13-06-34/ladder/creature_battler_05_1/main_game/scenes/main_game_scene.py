from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.turn_count = 0
        self.player_action = None
        self.bot_action = None

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
Turn: {self.turn_count}

{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.turn_count += 1
            self._player_choice_phase()
            self._bot_choice_phase()
            self._resolution_phase()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _player_choice_phase(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill_choice = self._choose_skill(self.player)
                if skill_choice:
                    self.player_action = ("attack", skill_choice)
                    break
            elif swap_button == choice:
                creature_choice = self._choose_creature_to_swap(self.player)
                if creature_choice:
                    self.player_action = ("swap", creature_choice)
                    break

    def _choose_skill(self, player):
        while True:
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            choices = skill_choices + [back_button]
            choice = self._wait_for_choice(player, choices)

            if choice == back_button:
                return None
            else:
                return choice.thing

    def _choose_creature_to_swap(self, player):
        while True:
            creature_choices = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
            back_button = Button("Back")
            choices = creature_choices + [back_button]
            
            if not creature_choices:
                self._show_text(player, "No other creatures available to swap!")
                return None

            choice = self._wait_for_choice(player, choices)

            if choice == back_button:
                return None
            else:
                return choice.thing

    def _bot_choice_phase(self):
        while True:
            if random.random() < 0.7:  # 70% chance to attack
                skill_choice = self._choose_skill(self.bot)
                if skill_choice:
                    self.bot_action = ("attack", skill_choice)
                    break
            else:
                creature_choice = self._choose_creature_to_swap(self.bot)
                if creature_choice:
                    self.bot_action = ("swap", creature_choice)
                    break

    def _resolution_phase(self):
        first, second = self._determine_turn_order()
        self._execute_action(*first)
        if self._check_battle_end():
            return
        self._execute_action(*second)

    def _determine_turn_order(self):
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        if player_speed > bot_speed or (player_speed == bot_speed and random.random() < 0.5):
            return (self.player, self.player_action), (self.bot, self.bot_action)
        else:
            return (self.bot, self.bot_action), (self.player, self.player_action)

    def _execute_action(self, actor, action):
        action_type, action_data = action
        if action_type == "swap":
            self._swap_creature(actor, action_data)
        elif action_type == "attack":
            self._use_skill(actor, action_data)

    def _swap_creature(self, actor, new_creature):
        actor.active_creature = new_creature
        self._show_text(self.player, f"{actor.display_name} swapped to {new_creature.display_name}!")

    def _use_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        elif self.player.active_creature.hp == 0:
            self._force_swap(self.player)
        elif self.bot.active_creature.hp == 0:
            self._force_swap(self.bot)
        return False

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            new_creature = random.choice(available_creatures)
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _end_battle(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
