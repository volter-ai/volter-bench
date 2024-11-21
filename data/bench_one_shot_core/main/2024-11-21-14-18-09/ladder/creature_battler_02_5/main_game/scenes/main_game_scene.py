from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_choice = None
        self.bot_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
ATK: {self.player_creature.attack} DEF: {self.player_creature.defense} SPD: {self.player_creature.speed}

{self.bot.display_name}'s {self.bot_creature.display_name}:
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
ATK: {self.bot_creature.attack} DEF: {self.bot_creature.defense} SPD: {self.bot_creature.speed}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            self.player_choice = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )

            # Bot choice phase
            self._show_text(self.bot, "Bot choosing skill...")
            self.bot_choice = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )

            # Resolution phase
            first = self.player
            second = self.bot
            first_creature = self.player_creature
            second_creature = self.bot_creature
            
            if self.bot_creature.speed > self.player_creature.speed or \
               (self.bot_creature.speed == self.player_creature.speed and random.random() < 0.5):
                first, second = second, first
                first_creature, second_creature = second_creature, first_creature

            # Execute skills
            for attacker, defender, creature, target in [
                (first, second, first_creature, second_creature),
                (second, first, second_creature, first_creature)
            ]:
                skill = creature.skills[0]  # Only tackle for now
                damage = creature.attack + skill.base_damage - target.defense  # FIXED: Now using defense instead of hp
                target.hp -= max(1, damage)  # Minimum 1 damage

                self._show_text(self.player, 
                    f"{creature.display_name} used {skill.display_name}! Dealt {damage} damage!")

                if target.hp <= 0:
                    winner = "You" if target == self.bot_creature else "Bot"
                    self._show_text(self.player, f"{winner} won the battle!")
                    self._transition_to_scene("MainMenuScene")
                    return
