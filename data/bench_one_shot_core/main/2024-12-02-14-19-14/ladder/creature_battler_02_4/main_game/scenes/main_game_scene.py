from mini_game_engine.engine.lib import AbstractGameScene, Button
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
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.player_chosen_skill = self.player_creature.skills[skill_choices.index(player_choice)]

            # Bot choice phase
            self._show_text(self.bot, "Bot choosing skill...")
            bot_choice = self._wait_for_choice(self.bot, [Button(skill.display_name) for skill in self.bot_creature.skills])
            self.bot_chosen_skill = self.bot_creature.skills[0]  # Bot only has tackle

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
        first, second = self.determine_order()
        self.execute_skill(first[0], first[1], first[2], first[3])
        if second[1].hp > 0:  # Only execute second skill if target still alive
            self.execute_skill(second[0], second[1], second[2], second[3])

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.bot_creature, self.player_creature, self.player_chosen_skill), \
                   (self.bot, self.player_creature, self.bot_creature, self.bot_chosen_skill)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.player_creature, self.bot_creature, self.bot_chosen_skill), \
                   (self.player, self.bot_creature, self.player_creature, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.bot_creature, self.player_creature, self.player_chosen_skill), \
                       (self.bot, self.player_creature, self.bot_creature, self.bot_chosen_skill)
            else:
                return (self.bot, self.player_creature, self.bot_creature, self.bot_chosen_skill), \
                       (self.player, self.bot_creature, self.player_creature, self.player_chosen_skill)

    def execute_skill(self, user, target, attacker, skill):
        damage = attacker.attack + skill.base_damage - target.defense
        target.hp -= damage
        self._show_text(user, f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")
