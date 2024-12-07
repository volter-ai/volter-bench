from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_chosen_skill = None
        self.bot_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_chosen_skill = self._wait_for_choice(self.player, skill_choices).thing

            # Bot choice phase
            self._show_text(self.bot, "Bot is choosing...")
            skill_choices = [SelectThing(skill) for skill in self.bot_creature.skills]
            self.bot_chosen_skill = self._wait_for_choice(self.bot, skill_choices).thing

            # Resolution phase
            self.resolve_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def resolve_turn(self):
        # Determine who goes first based on speed
        if self.player_creature.speed > self.bot_creature.speed:
            self.execute_attack(self.player, self.player_creature, self.player_chosen_skill, 
                              self.bot, self.bot_creature)
            if self.bot_creature.hp > 0:
                self.execute_attack(self.bot, self.bot_creature, self.bot_chosen_skill,
                                  self.player, self.player_creature)
        elif self.bot_creature.speed > self.player_creature.speed:
            self.execute_attack(self.bot, self.bot_creature, self.bot_chosen_skill,
                              self.player, self.player_creature)
            if self.player_creature.hp > 0:
                self.execute_attack(self.player, self.player_creature, self.player_chosen_skill,
                                  self.bot, self.bot_creature)
        else:
            # Random order if speeds are equal
            if random.random() < 0.5:
                self.execute_attack(self.player, self.player_creature, self.player_chosen_skill,
                                  self.bot, self.bot_creature)
                if self.bot_creature.hp > 0:
                    self.execute_attack(self.bot, self.bot_creature, self.bot_chosen_skill,
                                      self.player, self.player_creature)
            else:
                self.execute_attack(self.bot, self.bot_creature, self.bot_chosen_skill,
                                  self.player, self.player_creature)
                if self.player_creature.hp > 0:
                    self.execute_attack(self.player, self.player_creature, self.player_chosen_skill,
                                      self.bot, self.bot_creature)

    def execute_attack(self, attacker, attacker_creature, skill, defender, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= max(0, damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")
