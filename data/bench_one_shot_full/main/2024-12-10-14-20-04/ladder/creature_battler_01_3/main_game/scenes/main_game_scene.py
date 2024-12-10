from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = []

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe's {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild bot appeared!")
        
        while True:
            # Player phase
            player_skill = self._handle_player_turn()
            self.queued_skills.append((self.player, player_skill))

            # Bot phase  
            bot_skill = self._handle_bot_turn()
            self.queued_skills.append((self.bot, bot_skill))

            # Resolution phase
            self._resolve_skills()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return self.player_creature.skills[choices.index(choice)]

    def _handle_bot_turn(self):
        choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return self.bot_creature.skills[choices.index(choice)]

    def _resolve_skills(self):
        while self.queued_skills:
            attacker, skill = self.queued_skills.pop(0)
            target_creature = self.bot_creature if attacker == self.player else self.player_creature
            target = self.bot if attacker == self.player else self.player
            
            target_creature.hp -= skill.damage
            self._show_text(target, f"{attacker.display_name}'s {skill.display_name} dealt {skill.damage} damage!")
