from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.bot, "Battle Start!")

        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot Choice Phase
            self.bot_chosen_skill = self._get_skill_choice(self.bot, self.bot_creature)

            # Resolution Phase
            self._resolve_turn()

            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _resolve_turn(self):
        # Determine order based on speed
        if self.player_creature.speed > self.bot_creature.speed:
            first = (self.player, self.player_creature, self.player_chosen_skill)
            second = (self.bot, self.bot_creature, self.bot_chosen_skill)
        elif self.bot_creature.speed > self.player_creature.speed:
            first = (self.bot, self.bot_creature, self.bot_chosen_skill)
            second = (self.player, self.player_creature, self.player_chosen_skill)
        else:
            # Random if speeds are equal
            if random.random() < 0.5:
                first = (self.player, self.player_creature, self.player_chosen_skill)
                second = (self.bot, self.bot_creature, self.bot_chosen_skill)
            else:
                first = (self.bot, self.bot_creature, self.bot_chosen_skill)
                second = (self.player, self.player_creature, self.player_chosen_skill)

        # Execute moves in order
        self._execute_skill(*first, second[1])
        if second[1].hp > 0:  # Only execute second move if target still alive
            self._execute_skill(*second, first[1])

    def _execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= damage
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"Dealt {damage} damage!")
