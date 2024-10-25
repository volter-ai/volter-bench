from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random
from mini_game_engine.engine.lib import BotListener


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

    def _bot_turn(self):
        bot_creature = self.bot.active_creature
        if bot_creature.hp <= 0:
            available_creatures = [c for c in self.bot.creatures if c.hp > 0 and c != bot_creature]
            if available_creatures:
                self.bot_action = ("swap", random.choice(available_creatures))
            else:
                self.bot_action = None
        else:
            if random.random() < 0.2:  # 20% chance to swap
                available_creatures = [c for c in self.bot.creatures if c.hp > 0 and c != bot_creature]
                if available_creatures:
                    self.bot_action = ("swap", random.choice(available_creatures))
                else:
                    self.bot_action = ("attack", random.choice(bot_creature.skills))
            else:
                self.bot_action = ("attack", random.choice(bot_creature.skills))

    def _resolve_turn(self):
        if self.player_action[0] == "swap":
            self._perform_swap(self.player, self.player_action[1])
        if self.bot_action[0] == "swap":
            self._perform_swap(self.bot, self.bot_action[1])

        if self.player_action[0] == "attack" and self.bot_action[0] == "attack":
            if self.player.active_creature.speed >= self.bot.active_creature.speed:
                self._perform_attack(self.player, self.bot, self.player_action[1])
                if self.bot.active_creature.hp > 0:
                    self._perform_attack(self.bot, self.player, self.bot_action[1])
            else:
                self._perform_attack(self.bot, self.player, self.bot_action[1])
                if self.player.active_creature.hp > 0:
                    self._perform_attack(self.player, self.bot, self.player_action[1])
        elif self.player_action[0] == "attack":
            self._perform_attack(self.player, self.bot, self.player_action[1])
        elif self.bot_action[0] == "attack":
            self._perform_attack(self.bot, self.player, self.bot_action[1])

    def _perform_swap(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker: Player, defender: Player, skill: Skill):
        attacking_creature = attacker.active_creature
        defending_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = attacking_creature.attack + skill.base_damage - defending_creature.defense
        else:
            raw_damage = (attacking_creature.sp_attack / defending_creature.sp_defense) * skill.base_damage

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defending_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)

        defending_creature.hp = max(0, defending_creature.hp - final_damage)

        self._show_text(attacker, f"{attacking_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defending_creature.display_name} took {final_damage} damage!")

        if defending_creature.hp == 0:
            self._show_text(defender, f"{defending_creature.display_name} was knocked out!")
            self._force_swap(defender)

    def _calculate_weakness_factor(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def _force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if isinstance(player._listener, BotListener):
                new_creature = random.choice(available_creatures)
                self._perform_swap(player, new_creature)
            else:
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choice = self._wait_for_choice(player, creature_choices)
                self._perform_swap(player, creature_choice.thing)

    def _check_battle_end(self) -> bool:
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
