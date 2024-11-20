from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        
        while True:
            # Player turn
            player_skill = self._handle_turn(self.player, self.player_creature)
            
            # Bot turn
            bot_skill = self._handle_turn(self.bot, self.bot_creature)
            
            # Resolution phase
            self._resolve_skills(player_skill, bot_skill)
            
            # Check win conditions
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _handle_turn(self, current_player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        for i, choice in enumerate(choices):
            choice.value = {"skill": creature.skills[i]}
            
        choice = self._wait_for_choice(current_player, choices)
        return choice.value["skill"]

    def _resolve_skills(self, player_skill, bot_skill):
        # Apply damage
        self.bot_creature.hp -= player_skill.damage
        self.player_creature.hp -= bot_skill.damage
        
        self._show_text(self.player, 
            f"Your {self.player_creature.display_name} used {player_skill.display_name}!\n"
            f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")
