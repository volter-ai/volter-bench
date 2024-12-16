from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        # Reset creatures at start by setting hp to max_hp
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        
    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
{self.bot.display_name}'s {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player turn
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            
            # Bot turn
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills])

            # Resolve turns
            self._show_text(self.player, f"You used {player_skill.thing.display_name}!")
            self.bot_creature.hp -= player_skill.thing.damage

            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

            self._show_text(self.player, f"Foe used {bot_skill.thing.display_name}!")
            self.player_creature.hp -= bot_skill.thing.damage

            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")
