from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appears!")
        self._show_text(self.bot, f"Battle starts against {self.player_creature.display_name}!")

        while True:
            # Player turn
            player_skill = self._handle_turn(self.player, self.player_creature)
            bot_skill = self._handle_turn(self.bot, self.bot_creature)

            # Resolution phase
            self._resolve_skills(player_skill, bot_skill)

            if self._check_battle_end():
                break

    def _handle_turn(self, current_player: Player, creature: Creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _resolve_skills(self, player_skill, bot_skill):
        # Apply player skill
        self.bot_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.bot, f"Foe's {self.player_creature.display_name} used {player_skill.display_name}!")

        # Apply bot skill if still alive
        if self.bot_creature.hp > 0:
            self.player_creature.hp -= bot_skill.damage
            self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")
            self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {bot_skill.display_name}!")

    def _reset_creatures(self):
        # Reset both player and bot creatures to their original state
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def _check_battle_end(self):
        if self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.bot, "You lost!")
            self._reset_creatures()  # Reset before transitioning
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.bot, "You won!")
            self._reset_creatures()  # Reset before transitioning
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
