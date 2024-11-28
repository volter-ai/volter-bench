from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = []

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild bot appeared!")
        
        while True:
            # Player phase
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = next(s for s in self.player_creature.skills 
                              if s.display_name == player_choice.display_name)
            self.queued_skills.append((self.player, player_skill))

            # Bot phase
            bot_skill = self._wait_for_choice(self.bot, [Button(skill.display_name) 
                       for skill in self.bot_creature.skills])
            bot_skill = next(s for s in self.bot_creature.skills 
                           if s.display_name == bot_skill.display_name)
            self.queued_skills.append((self.bot, bot_skill))

            # Resolution phase
            for attacker, skill in self.queued_skills:
                if attacker == self.player:
                    self.bot_creature.hp -= skill.damage
                    self._show_text(self.player, 
                        f"Your {self.player_creature.display_name} used {skill.display_name}!")
                else:
                    self.player_creature.hp -= skill.damage
                    self._show_text(self.player,
                        f"Foe's {self.bot_creature.display_name} used {skill.display_name}!")

            self.queued_skills.clear()

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before exiting
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
