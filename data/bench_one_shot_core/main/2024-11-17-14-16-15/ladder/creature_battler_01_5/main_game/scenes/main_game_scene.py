from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creatures at start by setting hp to max_hp
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A battle begins!")
        
        while True:
            # Player turn
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing
            
            # Bot turn
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolve turns
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
            self.bot_creature.hp -= player_skill.damage
            
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, f"The foe {self.bot_creature.display_name} fainted! You win!")
                self._transition_to_scene("MainMenuScene")
                
            self._show_text(self.player, f"Foe {self.bot_creature.display_name} used {bot_skill.display_name}!")
            self.player_creature.hp -= bot_skill.damage
            
            if self.player_creature.hp <= 0:
                self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
                self._transition_to_scene("MainMenuScene")
