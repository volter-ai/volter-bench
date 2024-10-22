import random

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import (AbstractGameScene, Button,
                                         RandomModeGracefulExit, SelectThing)


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
        try:
            while True:
                actions = []
                for current_player in self.turn_order:
                    action = self._player_turn(current_player)
                    if action == "end_battle":
                        self._end_battle()
                        return
                    actions.append((current_player, action))

                self._resolve_turn(actions)

                if self._check_battle_end():
                    self._end_battle()
                    return
        except RandomModeGracefulExit:
            self._show_text(self.player, "Random mode ended. Returning to main menu.")
            self._end_battle()
        except Exception as e:
            self._show_text(self.player, f"An error occurred: {str(e)}")
            self._end_battle()

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
                    return ("attack", skill)
            elif choice == swap_button:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    return ("swap", new_creature)

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

    def _resolve_turn(self, actions):
        # Sort actions based on creature speed and action type
        sorted_actions = sorted(actions, key=lambda x: (x[0].active_creature.speed, x[1][0] == "swap"), reverse=True)
        
        # Resolve ties randomly
        i = 0
        while i < len(sorted_actions) - 1:
            if sorted_actions[i][0].active_creature.speed == sorted_actions[i+1][0].active_creature.speed:
                if random.choice([True, False]):
                    sorted_actions[i], sorted_actions[i+1] = sorted_actions[i+1], sorted_actions[i]
            i += 1

        for player, (action_type, target) in sorted_actions:
            if action_type == "swap":
                self._perform_swap(player, target)
            elif action_type == "attack":
                self._perform_attack(player, target)
            
            if self._check_forced_swap(player):
                return

    def _perform_swap(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker: Player, skill: Skill):
        defender = self.player if attacker == self.bot else self.bot
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

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

    def _check_forced_swap(self, player: Player):
        if player.active_creature.hp == 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    self._perform_swap(player, new_creature)
                    return False
            return True
        return False

    def _check_battle_end(self):
        for player in [self.player, self.bot]:
            if not any(creature.hp > 0 for creature in player.creatures):
                return True
        return False

    def _end_battle(self):
        winner = self.player if any(creature.hp > 0 for creature in self.player.creatures) else self.bot
        self._show_text(self.player, f"{winner.display_name} wins the battle!")
        self._transition_to_scene("MainMenuScene")
