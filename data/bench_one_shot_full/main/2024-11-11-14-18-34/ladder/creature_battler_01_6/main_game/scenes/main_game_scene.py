from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = []

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} (DMG: {skill.damage})" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A battle begins!")
        
        while True:
            # Player phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            self.queued_skills.append((self.player, player_skill.thing))

            # Bot phase  
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills])
            self.queued_skills.append((self.bot, bot_skill.thing))

            # Resolution phase
            for attacker, skill in self.queued_skills:
                if attacker == self.player:
                    target_creature = self.bot_creature
                    attacker_name = "You"
                else:
                    target_creature = self.player_creature
                    attacker_name = "Foe"
                
                target_creature.hp -= skill.damage
                self._show_text(self.player, f"{attacker_name} used {skill.display_name}!")
                
                if target_creature.hp <= 0:
                    target_creature.hp = 0
                    if attacker == self.player:
                        self._show_text(self.player, "You won!")
                    else:
                        self._show_text(self.player, "You lost!")
                    
                    # Reset creatures before transitioning
                    self.player_creature.hp = self.player_creature.max_hp
                    self.bot_creature.hp = self.bot_creature.max_hp
                    
                    self._transition_to_scene("MainMenuScene")
                    return

            self.queued_skills.clear()
