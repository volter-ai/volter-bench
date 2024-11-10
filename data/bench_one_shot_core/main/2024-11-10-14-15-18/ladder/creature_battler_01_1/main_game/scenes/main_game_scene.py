from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_skill_choice = None
        self.bot_skill_choice = None

    def __str__(self):
        player_creature = self.player.creatures[0]
        bot_creature = self.bot.creatures[0]
        
        return f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        self._show_text(self.bot, "A challenger approaches!")

        while True:
            # Player choice phase
            player_creature = self.player.creatures[0]
            choices = [SelectThing(skill) for skill in player_creature.skills]
            self.player_skill_choice = self._wait_for_choice(self.player, choices).thing

            # Bot choice phase  
            bot_creature = self.bot.creatures[0]
            bot_choices = [SelectThing(skill) for skill in bot_creature.skills]
            self.bot_skill_choice = self._wait_for_choice(self.bot, bot_choices).thing

            # Resolution phase
            self._resolve_turn()

            # Check win condition
            if self._check_battle_end():
                break

        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

        self._transition_to_scene("MainMenuScene")

    def _resolve_turn(self):
        player_creature = self.player.creatures[0]
        bot_creature = self.bot.creatures[0]

        # Player's skill
        bot_creature.hp -= self.player_skill_choice.damage
        self._show_text(self.player, f"Your {player_creature.display_name} used {self.player_skill_choice.display_name}!")
        self._show_text(self.bot, f"Foe's {player_creature.display_name} used {self.player_skill_choice.display_name}!")

        # Bot's skill
        player_creature.hp -= self.bot_skill_choice.damage
        self._show_text(self.player, f"Foe's {bot_creature.display_name} used {self.bot_skill_choice.display_name}!")
        self._show_text(self.bot, f"Your {bot_creature.display_name} used {self.bot_skill_choice.display_name}!")

    def _check_battle_end(self):
        player_creature = self.player.creatures[0]
        bot_creature = self.bot.creatures[0]

        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.bot, "You won the battle!")
            return True
        elif bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.bot, "You lost the battle!")
            return True
        return False
