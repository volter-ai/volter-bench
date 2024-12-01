from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

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
        self._show_text(self.player, "A wild trainer appears!")
        self._show_text(self.player, f"They send out {self.bot_creature.display_name}!")
        self._show_text(self.player, f"Go! {self.player_creature.display_name}!")

        while True:
            # Player phase
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.queued_skills.append((self.player, player_choice.thing))

            # Bot phase
            bot_choice = self._wait_for_choice(self.bot, skill_choices)
            self.queued_skills.append((self.bot, bot_choice.thing))

            # Resolution phase
            for attacker, skill in self.queued_skills:
                if attacker == self.player:
                    target = self.bot_creature
                    attacker_creature = self.player_creature
                else:
                    target = self.player_creature
                    attacker_creature = self.bot_creature

                self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
                target.hp = max(0, target.hp - skill.damage)

                if target.hp == 0:
                    if target == self.player_creature:
                        self._show_text(self.player, "You lost the battle!")
                    else:
                        self._show_text(self.player, "You won the battle!")
                    
                    # Reset creatures before returning to menu
                    self.player_creature.hp = self.player_creature.max_hp
                    self.bot_creature.hp = self.bot_creature.max_hp
                    self._transition_to_scene("MainMenuScene")
                    return

            self.queued_skills.clear()
