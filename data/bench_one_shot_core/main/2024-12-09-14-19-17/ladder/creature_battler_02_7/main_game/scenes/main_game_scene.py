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
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            self._show_text(self.player, "Choose your skill!")
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.player_choice = self.player_creature.skills[choices.index(player_choice)]

            # Bot Choice Phase
            self._show_text(self.bot, "Bot choosing skill...")
            bot_choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_choices)
            self.bot_choice = self.bot_creature.skills[bot_choices.index(bot_choice)]

            # Resolution Phase
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
        first, second = self.determine_turn_order()
        
        # First attack
        damage = self.calculate_damage(first[0], first[1], first[2])
        first[3].hp -= damage
        self._show_text(self.player, f"{first[0].display_name} used {first[1].display_name} for {damage} damage!")

        # Second attack (if target still alive)
        if first[3].hp > 0:
            damage = self.calculate_damage(second[0], second[1], second[2])
            second[3].hp -= damage
            self._show_text(self.player, f"{second[0].display_name} used {second[1].display_name} for {damage} damage!")

    def determine_turn_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player_creature, self.player_choice, self.bot_creature, self.bot_creature), \
                   (self.bot_creature, self.bot_choice, self.player_creature, self.player_creature)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot_creature, self.bot_choice, self.player_creature, self.player_creature), \
                   (self.player_creature, self.player_choice, self.bot_creature, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player_creature, self.player_choice, self.bot_creature, self.bot_creature), \
                       (self.bot_creature, self.bot_choice, self.player_creature, self.player_creature)
            else:
                return (self.bot_creature, self.bot_choice, self.player_creature, self.player_creature), \
                       (self.player_creature, self.player_choice, self.bot_creature, self.bot_creature)

    def calculate_damage(self, attacker, skill, defender):
        return max(0, attacker.attack + skill.base_damage - defender.defense)
