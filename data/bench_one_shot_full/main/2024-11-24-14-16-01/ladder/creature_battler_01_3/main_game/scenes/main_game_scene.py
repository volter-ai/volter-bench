from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_choice = None
        self.bot_choice = None
        self.phase = "player_choice"

    def __str__(self):
        status = f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe's {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

"""
        if self.phase == "player_choice":
            status += "\nChoose your skill:"
            for skill in self.player_creature.skills:
                status += f"\n> {skill.display_name} ({skill.damage} damage)"
        elif self.phase == "resolution":
            status += f"\nYou used {self.player_choice.display_name}!"
            status += f"\nFoe used {self.bot_choice.display_name}!"
        
        return status

    def run(self):
        while True:
            if self.phase == "player_choice":
                self.handle_player_choice()
            elif self.phase == "bot_choice":
                self.handle_bot_choice()
            elif self.phase == "resolution":
                self.handle_resolution()
                if self.check_battle_end():
                    return

    def handle_player_choice(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        self.player_choice = self._wait_for_choice(self.player, choices).thing
        self.phase = "bot_choice"

    def handle_bot_choice(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        self.bot_choice = self._wait_for_choice(self.bot, choices).thing
        self.phase = "resolution"

    def handle_resolution(self):
        self.bot_creature.hp -= self.player_choice.damage
        self.player_creature.hp -= self.bot_choice.damage
        self.phase = "player_choice"

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
