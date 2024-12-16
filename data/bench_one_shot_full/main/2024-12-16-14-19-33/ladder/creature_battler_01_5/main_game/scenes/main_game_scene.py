from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_choice = None
        self.bot_choice = None

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        self._show_text(self.player, f"They send out {self.bot_creature.display_name}!")
        self._show_text(self.player, f"Go! {self.player_creature.display_name}!")

        while True:
            # Player Choice Phase
            self.player_choice = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Bot Choice Phase
            self.bot_choice = self._wait_for_choice(
                self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]
            ).thing

            # Resolution Phase
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {self.player_choice.display_name}!")
            self.bot_creature.hp -= self.player_choice.damage

            if self.bot_creature.hp <= 0:
                self._show_text(self.player, f"The foe's {self.bot_creature.display_name} fainted!")
                self._show_text(self.player, "You won!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

            self._show_text(self.player, f"The foe's {self.bot_creature.display_name} used {self.bot_choice.display_name}!")
            self.player_creature.hp -= self.bot_choice.damage

            if self.player_creature.hp <= 0:
                self._show_text(self.player, f"Your {self.player_creature.display_name} fainted!")
                self._show_text(self.player, "You lost!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def _reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
