from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.bot.display_name}: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            player_action = self.player_choice_phase(self.player)
            bot_action = self.player_choice_phase(self.bot)
            self.resolution_phase(player_action, bot_action)

            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == attack_button:
            return self.choose_attack(current_player)
        elif choice == swap_button:
            return self.choose_swap(current_player)

    def choose_attack(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self.player_choice_phase(current_player)
        return ("attack", choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature != current_player.active_creature and creature.hp > 0]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self.player_choice_phase(current_player)
        return ("swap", choice.thing)

    def resolution_phase(self, player_action, bot_action):
        actions = [player_action, bot_action]
        random.shuffle(actions)

        for action in actions:
            if action[0] == "swap":
                self.perform_swap(self.player if action == player_action else self.bot, action[1])

        for action in sorted(actions, key=lambda x: self.get_creature_for_action(x, player_action, bot_action).speed if x[0] == "attack" else 0, reverse=True):
            if action[0] == "attack":
                attacker = self.player if action == player_action else self.bot
                defender = self.bot if attacker == self.player else self.player
                self.perform_attack(attacker, action[1])
                if defender.active_creature.hp == 0:
                    if not self.force_swap(defender):
                        return  # Battle ends if no swap is possible

    def get_creature_for_action(self, action, player_action, bot_action):
        if action == player_action:
            return self.player.active_creature
        elif action == bot_action:
            return self.bot.active_creature
        else:
            raise ValueError("Invalid action")

    def perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

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
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")
            return False
        
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        self._show_text(player, f"{player.active_creature.display_name} was knocked out! Choose a new creature:")
        choice = self._wait_for_choice(player, creature_choices)
        self.perform_swap(player, choice.thing)
        return True

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
