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
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            self._show_text(self.player, "Choose your skill!")
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.player_chosen_skill = self.player_creature.skills[skill_choices.index(player_choice)]

            # Bot Choice Phase
            self._show_text(self.bot, "Bot choosing skill...")
            bot_choice = self._wait_for_choice(self.bot, [Button(skill.display_name) for skill in self.bot_creature.skills])
            self.bot_chosen_skill = self.bot_creature.skills[0]  # Bot only has tackle

            # Resolution Phase
            first, second = self.determine_order()
            self.execute_turn(first)
            if not self.check_battle_end():
                self.execute_turn(second)
                if self.check_battle_end():
                    break
            else:
                break

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.bot)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.player)
        else:
            return random.choice([(self.player, self.bot), (self.bot, self.player)])

    def execute_turn(self, attacker):
        if attacker == self.player:
            damage = self.calculate_damage(self.player_creature, self.player_chosen_skill, self.bot_creature)
            self.bot_creature.hp -= damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {self.player_chosen_skill.display_name} for {damage} damage!")
            self._show_text(self.bot, f"Opponent's {self.player_creature.display_name} used {self.player_chosen_skill.display_name} for {damage} damage!")
        else:
            damage = self.calculate_damage(self.bot_creature, self.bot_chosen_skill, self.player_creature)
            self.player_creature.hp -= damage
            self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {self.bot_chosen_skill.display_name} for {damage} damage!")
            self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {self.bot_chosen_skill.display_name} for {damage} damage!")

    def calculate_damage(self, attacker, skill, defender):
        return max(0, attacker.attack + skill.base_damage - defender.defense)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.bot, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.bot, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
