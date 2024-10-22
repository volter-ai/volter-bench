from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        if self.player.creatures:
            self.player.active_creature = self.player.creatures[0]
        if self.bot.creatures:
            self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name if self.player.active_creature else 'No active creature'} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} if self.player.active_creature else 'N/A')
{self.bot.display_name}: {self.bot.active_creature.display_name if self.bot.active_creature else 'No active creature'} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} if self.bot.active_creature else 'N/A')

> Attack
> Swap
"""

    def run(self):
        while True:
            self.player_turn(self.player)
            if self.check_battle_end():
                break
            self.player_turn(self.bot)
            if self.check_battle_end():
                break
            self.resolution_phase()
            self.clear_chosen_skills()

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                skill = self.choose_skill(current_player)
                if skill:
                    current_player.active_creature.chosen_skill = skill
                    break
            elif choice == swap_button:
                new_creature = self.choose_creature(current_player)
                if new_creature:
                    current_player.active_creature.chosen_skill = None
                    current_player.active_creature = new_creature
                    break

    def choose_skill(self, player):
        choices = [SelectThing(skill, label=skill.display_name) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def choose_creature(self, player):
        choices = [SelectThing(creature, label=creature.display_name) 
                   for creature in player.creatures 
                   if creature != player.active_creature and creature.hp > 0]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def resolution_phase(self):
        first, second = self.determine_order()
        self.execute_action(first)
        if second.active_creature.hp > 0:
            self.execute_action(second)

    def determine_order(self):
        player_swap = self.player.active_creature.chosen_skill is None
        bot_swap = self.bot.active_creature.chosen_skill is None
        if player_swap or bot_swap:
            return (self.player, self.bot) if player_swap else (self.bot, self.player)
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return self.player, self.bot
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return self.bot, self.player
        else:
            return random.choice([(self.player, self.bot), (self.bot, self.player)])

    def execute_action(self, attacker):
        defender = self.bot if attacker == self.player else self.player
        if attacker.active_creature.chosen_skill is None:
            self._show_text(attacker, f"{attacker.display_name} swapped to {attacker.active_creature.display_name}!")
        else:
            skill = attacker.active_creature.chosen_skill
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")
        
        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

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
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if len(available_creatures) == 1:
                player.active_creature = available_creatures[0]
            else:
                new_creature = self.choose_creature(player)
                player.active_creature = new_creature
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def check_battle_end(self):
        player_creatures_fainted = all(c.hp == 0 for c in self.player.creatures)
        bot_creatures_fainted = all(c.hp == 0 for c in self.bot.creatures)

        if player_creatures_fainted and bot_creatures_fainted:
            self._show_text(self.player, "The battle ended in a tie!")
            return True
        elif player_creatures_fainted:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif bot_creatures_fainted:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def clear_chosen_skills(self):
        self.player.active_creature.chosen_skill = None
        self.bot.active_creature.chosen_skill = None

    def reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
            creature.chosen_skill = None
