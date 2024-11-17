from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A battle begins between {self.player.display_name} and {self.opponent.display_name}!")
        
        while True:
            # Player turn
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Bot turn
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Resolve turns
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
            self.opponent_creature.hp -= player_skill.damage
            
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, f"You won! {self.opponent_creature.display_name} fainted!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

            self._show_text(self.player, f"Foe {self.opponent_creature.display_name} used {opponent_skill.display_name}!")
            self.player_creature.hp -= opponent_skill.damage

            if self.player_creature.hp <= 0:
                self._show_text(self.player, f"You lost! {self.player_creature.display_name} fainted!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene") 
                return

    def _reset_creatures(self):
        """Reset creature HP to max after battle"""
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
