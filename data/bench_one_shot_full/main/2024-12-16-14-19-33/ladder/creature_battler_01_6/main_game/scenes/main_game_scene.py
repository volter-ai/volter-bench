from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_actions = []

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild creature appears!")
        
        while True:
            # Player phase
            player_skill = self._handle_turn(self.player, self.player_creature)
            self.queued_actions.append((self.player, player_skill))

            # Bot phase
            bot_skill = self._handle_turn(self.bot, self.bot_creature)
            self.queued_actions.append((self.bot, bot_skill))

            # Resolution phase
            self._resolve_actions()

            # Check win condition
            if self._check_battle_end():
                break

        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _handle_turn(self, current_player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return creature.skills[choices.index(choice)]

    def _resolve_actions(self):
        while self.queued_actions:
            attacker, skill = self.queued_actions.pop(0)
            target = self.bot_creature if attacker == self.player else self.player_creature
            target.hp = max(0, target.hp - skill.damage)
            self._show_text(self.player, f"{attacker.display_name}'s {skill.display_name} deals {skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
