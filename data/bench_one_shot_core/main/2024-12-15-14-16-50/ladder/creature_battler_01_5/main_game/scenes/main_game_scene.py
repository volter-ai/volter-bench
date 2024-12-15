from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        # Reset creatures at start of battle
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appears!")
        self._show_text(self.bot, f"Battle starts against {self.player_creature.display_name}!")

        while True:
            # Player turn
            player_choice = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            player_skill = player_choice.thing

            # Bot turn
            bot_choice = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills])
            bot_skill = bot_choice.thing

            # Resolution phase
            self.bot_creature.hp -= player_skill.damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
            
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.bot, "You lost!")
                break

            self.player_creature.hp -= bot_skill.damage
            self._show_text(self.player, f"Foe {self.bot_creature.display_name} used {bot_skill.display_name}!")

            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._show_text(self.bot, "You won!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
