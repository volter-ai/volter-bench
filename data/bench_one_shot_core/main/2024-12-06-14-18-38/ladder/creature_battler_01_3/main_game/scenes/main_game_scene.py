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
Foe's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} (DMG: {skill.damage})" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.bot, "Battle Start!")

        while True:
            # Player Choice Phase
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.queued_skills.append((self.player, player_choice.thing))

            # Bot Choice Phase
            bot_skill_choices = [SelectThing(skill) for skill in self.bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_skill_choices)
            self.queued_skills.append((self.bot, bot_choice.thing))

            # Resolution Phase
            for attacker, skill in self.queued_skills:
                defender = self.bot if attacker == self.player else self.player
                defender_creature = self.bot_creature if attacker == self.player else self.player_creature
                
                defender_creature.hp = max(0, defender_creature.hp - skill.damage)
                self._show_text(self.player, f"{attacker.display_name}'s {skill.display_name} deals {skill.damage} damage!")
                self._show_text(self.bot, f"{attacker.display_name}'s {skill.display_name} deals {skill.damage} damage!")

                if defender_creature.hp <= 0:
                    winner = self.player if defender == self.bot else self.bot
                    self._show_text(self.player, f"{'You won!' if winner == self.player else 'You lost!'}")
                    self._show_text(self.bot, f"{'You won!' if winner == self.bot else 'You lost!'}")
                    
                    # Reset creatures before transitioning
                    self.player_creature.hp = self.player_creature.max_hp
                    self.bot_creature.hp = self.bot_creature.max_hp
                    
                    self._transition_to_scene("MainMenuScene")
                    return

            self.queued_skills.clear()
