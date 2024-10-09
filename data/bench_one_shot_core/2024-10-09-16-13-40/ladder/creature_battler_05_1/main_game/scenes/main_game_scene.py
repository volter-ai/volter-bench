from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_order = [self.player, self.bot]
        random.shuffle(self.turn_order)

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
                    self._end_battle()
                    return

            self._resolve_turn()

            if self._check_battle_end():
                self._end_battle()
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
                    player.queued_action = ("attack", skill)
                    return
            elif choice == swap_button:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    player.queued_action = ("swap", new_creature)
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
        # Sort players by their active creature's speed, with random tiebreaker
        sorted_players = sorted(self.turn_order, key=lambda p: (p.active_creature.speed, random.random()), reverse=True)

        for player in sorted_players:
            opponent = self.bot if player == self.player else self.player
            action, target = player.queued_action

            if action == "swap":
                self._perform_swap(player, target)
                # Apply opponent's queued attack to the newly swapped-in creature
                if opponent.queued_action[0] == "attack":
                    self._perform_attack(opponent, opponent.queued_action[1], player.active_creature)
            elif action == "attack":
                # Only perform the attack if it hasn't been used on a swapped-in creature
                if opponent.queued_action[0] != "swap":
                    self._perform_attack(player, target)

            self._check_and_force_swap(opponent)

    def _perform_swap(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker: Player, skill: Skill, target_creature: Creature = None):
        if target_creature is None:
            target_creature = self.bot.active_creature if attacker == self.player else self.player.active_creature
        
        damage = self._calculate_damage(attacker.active_creature, target_creature, skill)
        target_creature.hp = max(0, target_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {target_creature.display_name}!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)

    def _get_type_factor(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_and_force_swap(self, player: Player):
        if player.active_creature.hp == 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                new_creature = available_creatures[0]
                self._perform_swap(player, new_creature)
            else:
                self._show_text(player, f"{player.display_name} has no more creatures able to fight!")

    def _check_battle_end(self):
        player_defeated = all(creature.hp == 0 for creature in self.player.creatures)
        bot_defeated = all(creature.hp == 0 for creature in self.bot.creatures)

        if player_defeated and bot_defeated:
            self._show_text(self.player, "The battle ends in a tie!")
            self._show_text(self.bot, "The battle ends in a tie!")
            return True
        elif player_defeated:
            self._show_text(self.player, f"{self.bot.display_name} wins the battle!")
            self._show_text(self.bot, f"{self.bot.display_name} wins the battle!")
            return True
        elif bot_defeated:
            self._show_text(self.player, f"{self.player.display_name} wins the battle!")
            self._show_text(self.bot, f"{self.player.display_name} wins the battle!")
            return True
        return False

    def _reset_creature_states(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp

    def _end_battle(self):
        self._show_text(self.player, "The battle has ended!")
        self._reset_creature_states()
        self._transition_to_scene("MainMenuScene")
