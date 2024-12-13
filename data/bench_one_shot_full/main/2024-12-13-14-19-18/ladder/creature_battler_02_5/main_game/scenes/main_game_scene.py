from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_choice = None
        self.bot_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.player_choice = self.player_creature.skills[choices.index(player_choice)]

            # Bot choice phase
            bot_choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_choices)
            self.bot_choice = self.bot_creature.skills[bot_choices.index(bot_choice)]

            # Resolution phase
            first, second = self.determine_order()
            self.resolve_attack(*first)
            if not self.check_battle_end():
                self.resolve_attack(*second)
                self.check_battle_end()

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_choice, self.bot_creature), (self.bot, self.bot_choice, self.player_creature)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_choice, self.player_creature), (self.player, self.player_choice, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_choice, self.bot_creature), (self.bot, self.bot_choice, self.player_creature)
            return (self.bot, self.bot_choice, self.player_creature), (self.player, self.player_choice, self.bot_creature)

    def resolve_attack(self, attacker, skill, target):
        damage = attacker.creatures[0].attack + skill.base_damage - target.defense
        damage = max(0, damage)
        target.hp -= damage
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._quit_whole_game()
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._quit_whole_game()
            return True
        return False
