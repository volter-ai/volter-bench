from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        # Reset creatures at start of battle
        self._reset_creatures(self.player)
        self._reset_creatures(self.bot)

        while True:
            # Player choice phase
            player_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Bot choice phase
            bot_skill = self._handle_player_turn(self.bot, self.bot_creature)

            # Resolution phase
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
            self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {bot_skill.display_name}!")
            
            self.bot_creature.hp -= player_skill.damage
            self.player_creature.hp -= bot_skill.damage

            # Check win conditions
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, current_player: Player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        
        # Find selected skill
        for skill in creature.skills:
            if skill.display_name == choice.display_name:
                return skill

    def _reset_creatures(self, player: Player):
        """Reset all creatures to max HP"""
        for creature in player.creatures:
            creature.hp = creature.max_hp
