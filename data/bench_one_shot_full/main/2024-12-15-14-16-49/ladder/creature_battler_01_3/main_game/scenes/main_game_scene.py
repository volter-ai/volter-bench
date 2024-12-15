from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = []

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        
        while True:
            # Player turn
            player_skill = self._handle_player_turn(self.player, self.player_creature)
            self.queued_skills.append((self.player, player_skill))

            # Bot turn
            bot_skill = self._handle_player_turn(self.bot, self.bot_creature)
            self.queued_skills.append((self.bot, bot_skill))

            # Resolution phase
            self._resolve_skills()

            # Check win condition
            if self._check_battle_end():
                break

        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, current_player, creature):
        skill_buttons = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, skill_buttons)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_skills(self):
        while self.queued_skills:
            player, skill = self.queued_skills.pop(0)
            target_creature = self.bot_creature if player == self.player else self.player_creature
            target_creature.hp = max(0, target_creature.hp - skill.damage)
            self._show_text(self.player, f"{player.display_name}'s {skill.display_name} deals {skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
