from mini_game_engine.engine.lib import AbstractGameScene, DictionaryChoice
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
            self.player_choice = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot Choice Phase
            self.bot_choice = self._get_skill_choice(self.bot, self.bot_creature)

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
        choices = []
        for skill in creature.skills:
            choice = DictionaryChoice(skill.display_name)
            choice.value = {"skill": skill}
            choices.append(choice)
        return self._wait_for_choice(player, choices).value["skill"]

    def _resolve_turn(self):
        # Determine order based on speed
        if self.player_creature.speed > self.bot_creature.speed:
            first = (self.player_creature, self.player_choice, self.bot_creature)
            second = (self.bot_creature, self.bot_choice, self.player_creature)
        elif self.bot_creature.speed > self.player_creature.speed:
            first = (self.bot_creature, self.bot_choice, self.player_creature)
            second = (self.player_creature, self.player_choice, self.bot_creature)
        else:
            if random.random() < 0.5:
                first = (self.player_creature, self.player_choice, self.bot_creature)
                second = (self.bot_creature, self.bot_choice, self.player_creature)
            else:
                first = (self.bot_creature, self.bot_choice, self.player_creature)
                second = (self.player_creature, self.player_choice, self.bot_creature)

        # Execute skills in order
        self._execute_skill(*first)
        if second[2].hp > 0:  # Only execute second skill if target still alive
            self._execute_skill(*second)

    def _execute_skill(self, attacker_creature, skill, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= damage
        message = f"{attacker_creature.display_name} used {skill.display_name}!"
        if attacker_creature == self.player_creature:
            self._show_text(self.player, message)
        else:
            self._show_text(self.bot, message)
