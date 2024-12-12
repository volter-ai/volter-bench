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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Bot Choice Phase
            self.bot_chosen_skill = self._wait_for_choice(
                self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]
            ).thing

            # Resolution Phase
            first, second = self.determine_order()
            
            # Execute first attack
            damage = self.calculate_damage(first[0], first[1], first[2], first[3])
            first[3].hp -= damage
            self._show_text(self.player, f"{first[0].display_name}'s {first[1].display_name} used {first[2].display_name} for {damage} damage!")
            
            if self.check_battle_end():
                return

            # Execute second attack
            damage = self.calculate_damage(second[0], second[1], second[2], second[3])
            second[3].hp -= damage
            self._show_text(self.player, f"{second[0].display_name}'s {second[1].display_name} used {second[2].display_name} for {damage} damage!")
            
            if self.check_battle_end():
                return

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_creature, self.player_chosen_skill, self.bot_creature), \
                   (self.bot, self.bot_creature, self.bot_chosen_skill, self.player_creature)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_creature, self.bot_chosen_skill, self.player_creature), \
                   (self.player, self.player_creature, self.player_chosen_skill, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.player_chosen_skill, self.bot_creature), \
                       (self.bot, self.bot_creature, self.bot_chosen_skill, self.player_creature)
            else:
                return (self.bot, self.bot_creature, self.bot_chosen_skill, self.player_creature), \
                       (self.player, self.player_creature, self.player_chosen_skill, self.bot_creature)

    def calculate_damage(self, attacker, attacker_creature, skill, defender_creature):
        return max(0, attacker_creature.attack + skill.base_damage - defender_creature.defense)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._quit_whole_game()
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._quit_whole_game()
            return True
        return False
