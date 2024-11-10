from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_queued_skill = None
        self.bot_queued_skill = None

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A battle begins!")
        
        while True:
            # Player phase
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_queued_skill = self._wait_for_choice(self.player, skill_choices).thing

            # Bot phase  
            self.bot_queued_skill = self._wait_for_choice(self.bot, 
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolution phase
            self._show_text(self.player, f"You used {self.player_queued_skill.display_name}!")
            self.bot_creature.hp -= self.player_queued_skill.damage
            
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

            self._show_text(self.player, f"Foe used {self.bot_queued_skill.display_name}!")
            self.player_creature.hp -= self.bot_queued_skill.damage

            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene") 
                return

    def _reset_creatures(self):
        """Reset creatures to initial state"""
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
