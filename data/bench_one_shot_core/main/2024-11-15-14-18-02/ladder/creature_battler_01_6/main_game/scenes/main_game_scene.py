from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice

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
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        # Reset creatures at start - logic moved here from model
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

        while True:
            # Player choice phase
            player_skill = self._handle_turn(self.player, self.player_creature)
            
            # Bot choice phase  
            bot_skill = self._handle_turn(self.bot, self.bot_creature)

            # Resolution phase
            self._show_text(self.player, f"You used {player_skill.display_name}!")
            self.bot_creature.hp -= player_skill.damage
            
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

            self._show_text(self.player, f"Foe used {bot_skill.display_name}!")
            self.player_creature.hp -= bot_skill.damage
            
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")

    def _handle_turn(self, current_player, current_creature):
        choices = []
        for skill in current_creature.skills:
            choice = DictionaryChoice(skill.display_name)
            choice.value = skill
            choices.append(choice)
        
        return self._wait_for_choice(current_player, choices).value
