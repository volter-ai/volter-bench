from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
from typing import List, Tuple

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
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        
        while True:
            # Initialize empty skill queue for this turn
            skill_queue: List[Tuple[Creature, Creature, Skill]] = []
            
            # Player Choice Phase
            self._show_text(self.player, "Your turn!")
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing
            skill_queue.append((self.player_creature, self.bot_creature, player_skill))
            
            # Foe Choice Phase
            self._show_text(self.player, "Foe's turn!")
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing
            skill_queue.append((self.bot_creature, self.player_creature, bot_skill))
            
            # Resolution Phase
            self._show_text(self.player, "Skills are being resolved!")
            for attacker, defender, skill in skill_queue:
                defender.hp -= skill.damage
                self._show_text(self.player, 
                    f"{attacker.display_name} used {skill.display_name}!")
                
                # Check for battle end after each skill resolution
                if defender.hp <= 0:
                    if defender == self.bot_creature:
                        self._show_text(self.player, "You won!")
                    else:
                        self._show_text(self.player, "You lost!")
                    self._transition_to_scene("MainMenuScene")
                    return

            # Clear skill queue at end of turn
            skill_queue.clear()
