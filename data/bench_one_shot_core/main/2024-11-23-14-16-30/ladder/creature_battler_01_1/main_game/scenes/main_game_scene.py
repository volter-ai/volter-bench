from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature

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
Foe {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        self._show_text(self.bot, "Battle start!")

        while True:
            # Player phase
            skill_buttons = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_buttons)
            player_skill = next(s for s in self.player_creature.skills 
                              if s.display_name == player_choice.display_name)
            self.queued_skills.append((self.player, player_skill))

            # Bot phase
            bot_skill = self.bot_creature.skills[0]  # Bot always uses first skill
            self.queued_skills.append((self.bot, bot_skill))

            # Resolution phase
            for attacker, skill in self.queued_skills:
                defender = self.bot_creature if attacker == self.player else self.player_creature
                defender.hp -= skill.damage
                self._show_text(self.player, 
                    f"{attacker.display_name}'s {skill.display_name} deals {skill.damage} damage!")
                
                if defender.hp <= 0:
                    winner = "You" if attacker == self.player else "Bot"
                    self._show_text(self.player, f"{winner} won the battle!")
                    self.player_creature.hp = self.player_creature.max_hp
                    self._transition_to_scene("MainMenuScene")
                    return

            self.queued_skills.clear()
