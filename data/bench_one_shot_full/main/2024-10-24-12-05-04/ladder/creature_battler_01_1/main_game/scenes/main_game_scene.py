from mini_game_engine.engine.lib import AbstractGameScene, Button
from collections import deque


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.skill_queue = deque()

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

Opponent's skills:
{self._format_skills(self.bot_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            # Player turn
            player_skill = self._player_turn()
            self.skill_queue.append((self.player, player_skill))
            
            # Bot turn
            bot_skill = self._bot_turn()
            self.skill_queue.append((self.bot, bot_skill))
            
            # Resolution phase
            self._resolve_turn()
            
            # Check for battle end
            if self._check_battle_end():
                break

    def _player_turn(self):
        self._show_text(self.player, "Your turn!")
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _bot_turn(self):
        self._show_text(self.bot, "Opponent's turn!")
        choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return next(skill for skill in self.bot_creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self):
        while self.skill_queue:
            attacker, skill = self.skill_queue.popleft()
            if attacker == self.player:
                self.bot_creature.hp -= skill.damage
                self._show_text(self.player, f"You used {skill.display_name}! It dealt {skill.damage} damage.")
            else:
                self.player_creature.hp -= skill.damage
                self._show_text(self.player, f"Opponent used {skill.display_name}! It dealt {skill.damage} damage.")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
