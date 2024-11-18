from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.phase = "player_choice"
        self.player_skill = None
        self.bot_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Phase: {self.phase}"""

    def run(self):
        while True:
            if self.phase == "player_choice":
                self._show_text(self.player, "Choose your skill!")
                skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
                self.player_skill = self._wait_for_choice(self.player, skill_choices).thing
                self.phase = "bot_choice"

            elif self.phase == "bot_choice":
                self._show_text(self.bot, "Bot choosing skill...")
                skill_choices = [SelectThing(skill) for skill in self.bot_creature.skills]
                self.bot_skill = self._wait_for_choice(self.bot, skill_choices).thing
                self.phase = "resolution"

            elif self.phase == "resolution":
                # Determine order
                first = self.player
                second = self.bot
                first_skill = self.player_skill
                second_skill = self.bot_skill
                first_creature = self.player_creature
                second_creature = self.bot_creature

                if self.bot_creature.speed > self.player_creature.speed or \
                   (self.bot_creature.speed == self.player_creature.speed and random.random() < 0.5):
                    first, second = second, first
                    first_skill, second_skill = second_skill, first_skill
                    first_creature, second_creature = second_creature, first_creature

                # Execute skills
                for attacker, skill, attacker_creature, defender_creature in [
                    (first, first_skill, first_creature, second_creature),
                    (second, second_skill, second_creature, first_creature)
                ]:
                    if defender_creature.hp <= 0:
                        continue

                    # Calculate damage
                    if skill.is_physical:
                        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
                    else:
                        raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

                    # Type effectiveness
                    effectiveness = 1.0
                    if skill.skill_type == "fire":
                        if defender_creature.creature_type == "leaf":
                            effectiveness = 2.0
                        elif defender_creature.creature_type == "water":
                            effectiveness = 0.5
                    elif skill.skill_type == "water":
                        if defender_creature.creature_type == "fire":
                            effectiveness = 2.0
                        elif defender_creature.creature_type == "leaf":
                            effectiveness = 0.5
                    elif skill.skill_type == "leaf":
                        if defender_creature.creature_type == "water":
                            effectiveness = 2.0
                        elif defender_creature.creature_type == "fire":
                            effectiveness = 0.5

                    final_damage = int(raw_damage * effectiveness)
                    defender_creature.hp = max(0, defender_creature.hp - final_damage)

                    self._show_text(self.player, 
                        f"{attacker_creature.display_name} used {skill.display_name}! "
                        f"Dealt {final_damage} damage!")

                    if defender_creature.hp <= 0:
                        winner = attacker
                        self._show_text(self.player,
                            f"{defender_creature.display_name} fainted! "
                            f"{winner.display_name} wins!")
                        
                        # Reset creatures by setting hp back to max_hp
                        self.player_creature.hp = self.player_creature.max_hp
                        self.bot_creature.hp = self.bot_creature.max_hp
                        
                        self._transition_to_scene("MainMenuScene")
                        return

                self.phase = "player_choice"
