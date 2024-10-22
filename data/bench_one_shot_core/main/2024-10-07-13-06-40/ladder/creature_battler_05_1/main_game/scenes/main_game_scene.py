from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
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
            choice = self._wait_for_choice(self.player, [Button("Attack"), Button("Swap")])
            if choice.display_name == "Attack":
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices + [Button("Back")])
                if isinstance(skill_choice, SelectThing):
                    self.player_action = ("attack", skill_choice.thing)
                    break
            elif choice.display_name == "Swap":
                creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
                creature_choice = self._wait_for_choice(self.player, creature_choices + [Button("Back")])
                if isinstance(creature_choice, SelectThing):
                    self.player_action = ("swap", creature_choice.thing)
                    break

    def _bot_choice_phase(self):
        bot_creature = self.bot.active_creature
        if bot_creature.hp <= 0:
            available_creatures = [c for c in self.bot.creatures if c.hp > 0 and c != bot_creature]
            if available_creatures:
                self.bot_action = ("swap", random.choice(available_creatures))
        else:
            if random.random() < 0.2:  # 20% chance to swap
                available_creatures = [c for c in self.bot.creatures if c.hp > 0 and c != bot_creature]
                if available_creatures:
                    self.bot_action = ("swap", random.choice(available_creatures))
            else:
                self.bot_action = ("attack", random.choice(bot_creature.skills))

    def _resolution_phase(self):
        player_first = self._determine_turn_order()
        actions = [self.player_action, self.bot_action]
        actors = [self.player, self.bot]
        
        if player_first:
            self._execute_action(self.player, self.bot, *self.player_action)
            if self.bot.active_creature.hp > 0:
                self._execute_action(self.bot, self.player, *self.bot_action)
        else:
            self._execute_action(self.bot, self.player, *self.bot_action)
            if self.player.active_creature.hp > 0:
                self._execute_action(self.player, self.bot, *self.player_action)

        self._show_text(self.player, self.__str__())
        self._show_text(self.bot, self.__str__())

    def _determine_turn_order(self):
        if self.player_action[0] == "swap" or self.bot_action[0] == "swap":
            return self.player_action[0] == "swap"
        return self.player.active_creature.speed >= self.bot.active_creature.speed

    def _execute_action(self, attacker: Player, defender: Player, action_type: str, action_target: Creature | Skill):
        if action_type == "attack":
            self._execute_attack(attacker, defender, action_target)
        elif action_type == "swap":
            attacker.active_creature = action_target
            self._show_text(attacker, f"{attacker.display_name} swapped to {action_target.display_name}!")
            self._show_text(defender, f"{attacker.display_name} swapped to {action_target.display_name}!")

    def _execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")
        self._show_text(defender, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self) -> bool:
        if all(creature.hp <= 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.bot, "You won the battle!")
            return True
        elif all(creature.hp <= 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.bot, "You lost the battle!")
            return True
        return False

    def _end_battle(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
