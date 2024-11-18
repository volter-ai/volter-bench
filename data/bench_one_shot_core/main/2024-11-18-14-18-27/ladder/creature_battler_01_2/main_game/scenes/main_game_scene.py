from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild creature appears!")
        
        while True:
            # Player turn
            player_skill = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )
            
            # Bot turn
            bot_skill = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )

            # Resolution phase
            for skill_name, attacker, defender in [
                (player_skill.display_name, self.player_creature, self.bot_creature),
                (bot_skill.display_name, self.bot_creature, self.player_creature)
            ]:
                skill = next(s for s in attacker.skills if s.display_name == skill_name)
                defender.hp -= skill.damage
                self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
                
                if defender.hp <= 0:
                    winner = self.player if defender == self.bot_creature else self.bot
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    # Reset creatures' HP before transitioning
                    self.player_creature.hp = self.player_creature.max_hp
                    self.bot_creature.hp = self.bot_creature.max_hp
                    self._transition_to_scene("MainMenuScene")
                    return
