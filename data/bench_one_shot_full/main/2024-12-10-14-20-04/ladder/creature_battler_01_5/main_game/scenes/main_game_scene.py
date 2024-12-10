from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_actions = []

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A battle begins between {self.player.display_name} and {self.bot.display_name}!")
        self._show_text(self.bot, f"A battle begins between {self.player.display_name} and {self.bot.display_name}!")

        while True:
            # Player phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            self.queued_actions.append((self.player, player_skill.thing))

            # Bot phase
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills])
            self.queued_actions.append((self.bot, bot_skill.thing))

            # Resolution phase
            for attacker, skill in self.queued_actions:
                if attacker == self.player:
                    target_creature = self.bot_creature
                    target = self.bot
                else:
                    target_creature = self.player_creature
                    target = self.player

                target_creature.hp -= skill.damage
                self._show_text(self.player, f"{attacker.display_name}'s {skill.display_name} hits for {skill.damage} damage!")
                self._show_text(self.bot, f"{attacker.display_name}'s {skill.display_name} hits for {skill.damage} damage!")

                if target_creature.hp <= 0:
                    if target == self.bot:
                        self._show_text(self.player, "You won!")
                        self._show_text(self.bot, "You lost!")
                    else:
                        self._show_text(self.player, "You lost!")
                        self._show_text(self.bot, "You won!")
                    
                    # Reset creatures before transitioning
                    self.player_creature.hp = self.player_creature.max_hp
                    self.bot_creature.hp = self.bot_creature.max_hp
                    self._transition_to_scene("MainMenuScene")
                    return

            self.queued_actions.clear()
