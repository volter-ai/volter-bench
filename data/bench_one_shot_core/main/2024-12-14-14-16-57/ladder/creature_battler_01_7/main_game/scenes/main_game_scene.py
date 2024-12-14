from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creatures at start
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild creature appears!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.get_skill_choice(self.player, self.player_creature)
            
            # Bot Choice Phase  
            bot_skill = self.get_skill_choice(self.bot, self.bot_creature)

            # Resolution Phase
            self._show_text(self.player, f"You used {player_skill.display_name}!")
            self.bot_creature.hp -= player_skill.damage

            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return

            self._show_text(self.player, f"Foe used {bot_skill.display_name}!")
            self.player_creature.hp -= bot_skill.damage

            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene") 
                return

    def get_skill_choice(self, player, creature):
        choices = [
            DictionaryChoice(skill.display_name) for skill in creature.skills
        ]
        for choice, skill in zip(choices, creature.skills):
            choice.value = {"skill": skill}
            
        return self._wait_for_choice(player, choices).value["skill"]
