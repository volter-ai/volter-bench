from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        # Reset creatures to full HP
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player turn
            player_skill = self._handle_player_turn(self.player)
            bot_skill = self._handle_player_turn(self.bot)

            # Resolution phase
            self._resolve_turn(player_skill, bot_skill)

            # Check win condition
            if self._check_battle_end():
                break

    def _handle_player_turn(self, current_player: Player) -> SelectThing:
        creature = self.player_creature if current_player == self.player else self.bot_creature
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(current_player, choices)

    def _resolve_turn(self, player_skill, bot_skill):
        # Apply damage
        self.bot_creature.hp -= player_skill.thing.damage
        self.player_creature.hp -= bot_skill.thing.damage

        # Show results
        self._show_text(self.player, 
            f"Your {self.player_creature.display_name} used {player_skill.thing.display_name}!\n"
            f"Foe's {self.bot_creature.display_name} used {bot_skill.thing.display_name}!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
