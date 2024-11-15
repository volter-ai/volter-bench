from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = []

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appears!")
        self._show_text(self.bot, f"Battle starts against {self.player_creature.display_name}!")

        while True:
            # Player phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            player_skill = player_choice.thing

            # Bot phase
            bot_choice = self._wait_for_choice(self.bot, [SelectThing(skill) for skill in self.bot_creature.skills])
            bot_skill = bot_choice.thing

            # Resolution phase
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
            self.bot_creature.hp -= player_skill.damage

            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.bot, "You lost!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

            self._show_text(self.player, f"Foe {self.bot_creature.display_name} used {bot_skill.display_name}!")
            self.player_creature.hp -= bot_skill.damage

            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._show_text(self.bot, "You won!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
