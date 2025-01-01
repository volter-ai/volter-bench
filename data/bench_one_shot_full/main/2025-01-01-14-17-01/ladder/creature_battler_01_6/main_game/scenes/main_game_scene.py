from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
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
"""

    def run(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            if self.check_battle_end():
                break

        # Reset the player's creatures' state after the battle
        self.reset_player_creatures()

        # After the battle ends, ask the player if they want to return to the main menu or quit
        self.post_battle_options()

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
        bot_creature.hp -= self.player_choice.thing.damage
        player_creature.hp -= self.bot_choice.thing.damage

    def check_battle_end(self):
        player_creature = self.player.creatures[0]
        bot_creature = self.bot.creatures[0]
        if player_creature.hp <= 0 or bot_creature.hp <= 0:
            if player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
            else:
                self._show_text(self.player, "You won!")
            return True
        return False

    def reset_player_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp

    def post_battle_options(self):
        return_to_menu_button = Button("Return to Main Menu")
        quit_button = Button("Quit")
        choices = [return_to_menu_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == return_to_menu_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
