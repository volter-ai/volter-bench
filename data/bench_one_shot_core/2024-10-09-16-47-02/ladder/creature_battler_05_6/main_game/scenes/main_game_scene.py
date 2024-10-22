import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        self.player_chosen_action = None
        self.bot_chosen_action = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.bot.display_name}: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            self.player_choice_phase(self.player)
            self.player_choice_phase(self.bot)
            self.resolution_phase()
            
            if self.check_battle_end():
                break
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                skill = self.choose_skill(current_player)
                if skill:
                    if current_player == self.player:
                        self.player_chosen_action = ("attack", skill)
                    else:
                        self.bot_chosen_action = ("attack", skill)
                    break
            elif choice == swap_button:
                new_creature = self.choose_creature(current_player)
                if new_creature:
                    if current_player == self.player:
                        self.player_chosen_action = ("swap", new_creature)
                    else:
                        self.bot_chosen_action = ("swap", new_creature)
                    break

    def choose_skill(self, player):
        skills = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices = skills + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if choice != back_button else None

    def choose_creature(self, player):
        available_creatures = [creature for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        creatures = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creatures + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if choice != back_button else None

    def resolution_phase(self):
        players = [self.player, self.bot]
        actions = [self.player_chosen_action, self.bot_chosen_action]
        
        # Sort players by speed of their active creatures, with random factor for equal speeds
        players_actions = list(zip(players, actions))
        players_actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)
        
        for player, action in players_actions:
            opponent = self.bot if player == self.player else self.player
            action_type, target = action

            if action_type == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action_type == "attack":
                damage = self.calculate_damage(player.active_creature, opponent.active_creature, target)
                opponent.active_creature.hp = max(0, opponent.active_creature.hp - damage)
                self._show_text(player, f"{player.active_creature.display_name} used {target.display_name} and dealt {damage} damage!")

            if opponent.active_creature.hp == 0:
                self.force_swap(opponent)

        # Reset chosen actions
        self.player_chosen_action = None
        self.bot_chosen_action = None

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)  # Explicitly convert to integer
        return max(1, final_damage)

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return False

        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
        else:
            new_creature = self.choose_creature(player)
            if new_creature:
                player.active_creature = new_creature
            else:
                player.active_creature = available_creatures[0]

        self._show_text(player, f"{player.display_name} swapped to {player.active_creature.display_name}!")
        return True

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False
