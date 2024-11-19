from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_chosen_skill = None
        self.bot_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.bot, "Battle Start!")

        while True:
            # Player Choice Phase
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.player_chosen_skill = self.player_creature.skills[choices.index(player_choice)]

            # Bot Choice Phase
            bot_choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_choices)
            self.bot_chosen_skill = self.bot_creature.skills[bot_choices.index(bot_choice)]

            # Resolution Phase
            first, second = self.determine_order()
            self.execute_turn(first)
            if not self.check_battle_end():
                self.execute_turn(second)
                if self.check_battle_end():
                    break
            else:
                break

        self._transition_to_scene("MainMenuScene")

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_chosen_skill), (self.bot, self.bot_chosen_skill)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_chosen_skill), (self.player, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_chosen_skill), (self.bot, self.bot_chosen_skill)
            return (self.bot, self.bot_chosen_skill), (self.player, self.player_chosen_skill)

    def execute_turn(self, turn_data):
        attacker, skill = turn_data
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.bot_creature
        else:
            attacker_creature = self.bot_creature
            defender_creature = self.player_creature

        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= max(1, damage)  # Minimum 1 damage

        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.bot, f"{attacker_creature.display_name} used {skill.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.bot, "You won!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.bot, "You lost!")
            return True
        return False
