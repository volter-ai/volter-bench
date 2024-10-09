from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random


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

{self.player.display_name}'s {player_creature.display_name}
HP: {player_creature.hp}/{player_creature.max_hp}

{self.bot.display_name}'s {bot_creature.display_name}
HP: {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.turn_counter += 1
            self._player_turn()
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

    def _choose_skill(self, actor: Player):
        back_button = Button("Back")
        skill_choices = [SelectThing(skill) for skill in actor.active_creature.skills] + [back_button]
        skill_choice = self._wait_for_choice(actor, skill_choices)
        if skill_choice == back_button:
            return None
        return skill_choice.thing

    def _choose_creature_to_swap(self, actor: Player):
        back_button = Button("Back")
        creature_choices = [SelectThing(creature) for creature in actor.creatures 
                            if creature != actor.active_creature and creature.hp > 0] + [back_button]
        if len(creature_choices) == 1:  # Only "Back" button
            self._show_text(actor, "No other creatures available to swap!")
            return None
        creature_choice = self._wait_for_choice(actor, creature_choices)
        if creature_choice == back_button:
            return None
        return creature_choice.thing

    def _bot_turn(self):
        while True:
            if random.random() < 0.2:
                creature_choice = self._choose_creature_to_swap(self.bot)
                if creature_choice:
                    self.bot_action = ("swap", creature_choice)
                    break
            else:
                skill_choice = self._choose_skill(self.bot)
                if skill_choice:
                    self.bot_action = ("attack", skill_choice)
                    break

    def _resolve_turn(self):
        first, second = self._determine_turn_order()
        
        # Handle swaps first
        if first[1][0] == "swap":
            self._execute_action(*first)
            self._execute_queued_attack(second[0], second[1][1])
        elif second[1][0] == "swap":
            self._execute_action(*second)
            self._execute_queued_attack(first[0], first[1][1])
        else:
            # If no swaps, execute actions in speed order
            self._execute_action(*first)
            if not self._check_battle_end():
                self._execute_action(*second)

        self._check_and_force_swap(first[0])
        self._check_and_force_swap(second[0])

    def _determine_turn_order(self):
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        if player_speed > bot_speed or (player_speed == bot_speed and random.random() < 0.5):
            return (self.player, self.player_action), (self.bot, self.bot_action)
        else:
            return (self.bot, self.bot_action), (self.player, self.player_action)

    def _execute_action(self, actor: Player, action):
        action_type, action_object = action
        if action_type == "swap":
            actor.active_creature = action_object
            self._show_text(self.player, f"{actor.display_name} swapped to {action_object.display_name}!")
        elif action_type == "attack":
            self._execute_attack(actor, action_object)

    def _execute_attack(self, attacker: Player, skill: Skill):
        attacking_creature = attacker.active_creature
        defending_player = self.bot if attacker == self.player else self.player
        defending_creature = defending_player.active_creature
        damage = self._calculate_damage(attacking_creature, defending_creature, skill)
        defending_creature.hp = max(0, defending_creature.hp - damage)
        self._show_text(self.player, f"{attacking_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defending_creature.display_name}!")

    def _execute_queued_attack(self, attacker: Player, skill: Skill):
        self._execute_attack(attacker, skill)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)
        
        type_effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_effectiveness(self, skill_type: str, defender_type: str):
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1.0)

    def _check_and_force_swap(self, actor: Player):
        if actor.active_creature.hp == 0:
            available_creatures = [c for c in actor.creatures if c.hp > 0]
            if available_creatures:
                if actor == self.player:
                    self._show_text(actor, f"{actor.active_creature.display_name} has fainted! Choose a new creature.")
                    new_creature = self._choose_creature_to_swap(actor)
                    while new_creature is None:
                        self._show_text(actor, "You must choose a new creature!")
                        new_creature = self._choose_creature_to_swap(actor)
                else:
                    new_creature = random.choice(available_creatures)
                actor.active_creature = new_creature
                self._show_text(self.player, f"{actor.display_name} sent out {new_creature.display_name}!")

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
