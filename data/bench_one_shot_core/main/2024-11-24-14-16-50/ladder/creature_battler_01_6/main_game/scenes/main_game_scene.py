from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = []

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            player_skill = self._handle_turn(self.player, self.player_creature)
            
            # Bot Choice Phase
            bot_skill = self._handle_turn(self.bot, self.bot_creature)
            
            # Resolution Phase
            self._resolve_skills(player_skill, bot_skill)
            
            # Check win conditions
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

    def _handle_turn(self, current_player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        for i, skill in enumerate(creature.skills):
            choices[i].value = {"skill": skill}
        
        choice = self._wait_for_choice(current_player, choices)
        return choice.value["skill"]

    def _resolve_skills(self, player_skill, bot_skill):
        # Apply damage
        self.bot_creature.hp -= player_skill.damage
        self.player_creature.hp -= bot_skill.damage
        
        self._show_text(self.player, 
            f"Your {self.player_creature.display_name} used {player_skill.display_name}!\n"
            f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")
