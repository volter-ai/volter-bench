from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.reset_creatures()

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} (DMG: {skill.damage})" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        self._show_text(self.player, f"They send out {self.bot_creature.display_name}!")
        self._show_text(self.player, f"Go! {self.player_creature.display_name}!")
        
        self.battle_loop()

    def battle_loop(self):
        while True:
            # Player turn
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            
            # Bot turn
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills])

            # Resolution phase
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.thing.display_name}!")
            self.bot_creature.hp -= player_skill.thing.damage

            if self.bot_creature.hp <= 0:
                self._show_text(self.player, f"The foe's {self.bot_creature.display_name} fainted!")
                self._show_text(self.player, "You won!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

            self._show_text(self.player, f"The foe's {self.bot_creature.display_name} used {bot_skill.thing.display_name}!")
            self.player_creature.hp -= bot_skill.thing.damage

            if self.player_creature.hp <= 0:
                self._show_text(self.player, f"Your {self.player_creature.display_name} fainted!")
                self._show_text(self.player, "You lost!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
