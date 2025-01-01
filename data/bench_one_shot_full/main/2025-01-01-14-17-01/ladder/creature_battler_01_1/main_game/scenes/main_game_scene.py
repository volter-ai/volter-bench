from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")

    def __str__(self):
        player_creature = self.player.creatures[0]
        bot_creature = self.bot.creatures[0]
        return f"""=== Main Game Scene ===
Player Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})
Bot Creature: {bot_creature.display_name} (HP: {bot_creature.hp}/{bot_creature.max_hp})

Choose a skill:
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.bot.creatures[0].hp > 0:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

        self.end_battle()

    def player_choice_phase(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        self.player_choice = self._wait_for_choice(self.player, choices)

    def foe_choice_phase(self):
        bot_creature = self.bot.creatures[0]
        choices = [SelectThing(skill) for skill in bot_creature.skills]
        self.bot_choice = self._wait_for_choice(self.bot, choices)

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        bot_creature = self.bot.creatures[0]

        # Player's skill effect
        bot_creature.hp -= self.player_choice.thing.damage

        # Bot's skill effect
        player_creature.hp -= self.bot_choice.thing.damage

    def end_battle(self):
        if self.player.creatures[0].hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
        
        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
