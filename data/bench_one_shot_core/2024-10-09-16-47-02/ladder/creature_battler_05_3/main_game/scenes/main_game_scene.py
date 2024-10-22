import random

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_order = [self.player, self.bot]
        random.shuffle(self.turn_order)
        self.player_action = None
        self.bot_action = None

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
            for current_player in self.turn_order:
                action = self._player_turn(current_player)
                if action == "end_battle":
                    return

            if self._resolve_turn():
                return

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        self._show_text(self.player, f"{self.player.display_name} sends out {self.player.active_creature.display_name}!")
        self._show_text(self.bot, f"{self.bot.display_name} sends out {self.bot.active_creature.display_name}!")

    def _player_turn(self, player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                skill = self._choose_skill(player)
                if skill:
                    if player == self.player:
                        self.player_action = ("attack", skill)
                    else:
                        self.bot_action = ("attack", skill)
                    return
            elif choice == swap_button:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    if player == self.player:
                        self.player_action = ("swap", new_creature)
                    else:
                        self.bot_action = ("swap", new_creature)
                    return

    def _choose_skill(self, player: Player):
        skills = player.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(player, choices)

        if choice == back_button:
            return None
        return choice.thing

    def _choose_swap_creature(self, player: Player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(player, choices)

        if choice == back_button:
            return None
        return choice.thing

    def _resolve_turn(self):
        # Execute swap actions first
        for player, action in [(self.player, self.player_action), (self.bot, self.bot_action)]:
            if action[0] == "swap":
                self._perform_swap(player, action[1])

        # Determine skill execution order based on speed
        skill_actions = []
        for player, action in [(self.player, self.player_action), (self.bot, self.bot_action)]:
            if action[0] == "attack":
                skill_actions.append((player, action[1]))

        skill_actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)

        # Resolve ties randomly
        if len(skill_actions) == 2 and skill_actions[0][0].active_creature.speed == skill_actions[1][0].active_creature.speed:
            random.shuffle(skill_actions)

        # Execute skills
        for player, skill in skill_actions:
            if self._perform_attack(player, skill) == "end_battle":
                return True

        self.player_action = None
        self.bot_action = None

        return self._check_battle_end()

    def _perform_swap(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker: Player, skill: Skill):
        defender = self.player if attacker == self.bot else self.bot
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
            if not self._force_swap(defender):
                return "end_battle"

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)  # Explicit conversion to integer
        return max(1, final_damage)

    def _get_type_factor(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
        new_creature = available_creatures[0]
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} sends out {new_creature.display_name}!")
        return True

    def _check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                self._transition_to_scene("MainMenuScene")
                return True
        return False
