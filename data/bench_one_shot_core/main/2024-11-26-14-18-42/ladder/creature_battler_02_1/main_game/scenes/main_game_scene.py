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
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

VS

{self.bot.display_name}'s {self.bot_creature.display_name}:
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Attack: {self.bot_creature.attack}
Defense: {self.bot_creature.defense}
Speed: {self.bot_creature.speed}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.player_chosen_skill = self.player_creature.skills[choices.index(player_choice)]

            # Bot Choice Phase
            bot_choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_choices)
            self.bot_chosen_skill = self.bot_creature.skills[bot_choices.index(bot_choice)]

            # Resolution Phase
            first, second = self.determine_turn_order()
            
            # Execute first attack
            damage = self.calculate_damage(first[0], first[1], first[2])
            first[3].hp -= damage
            self._show_text(self.player, f"{first[0].display_name} used {first[1].display_name} for {damage} damage!")

            if first[3].hp <= 0:
                self.handle_battle_end(first[3] == self.bot_creature)
                return

            # Execute second attack
            damage = self.calculate_damage(second[0], second[1], second[2])
            second[3].hp -= damage
            self._show_text(self.player, f"{second[0].display_name} used {second[1].display_name} for {damage} damage!")

            if second[3].hp <= 0:
                self.handle_battle_end(second[3] == self.bot_creature)
                return

    def determine_turn_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player_creature, self.player_chosen_skill, self.bot_creature, self.bot_creature), \
                   (self.bot_creature, self.bot_chosen_skill, self.player_creature, self.player_creature)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot_creature, self.bot_chosen_skill, self.player_creature, self.player_creature), \
                   (self.player_creature, self.player_chosen_skill, self.bot_creature, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player_creature, self.player_chosen_skill, self.bot_creature, self.bot_creature), \
                       (self.bot_creature, self.bot_chosen_skill, self.player_creature, self.player_creature)
            else:
                return (self.bot_creature, self.bot_chosen_skill, self.player_creature, self.player_creature), \
                       (self.player_creature, self.player_chosen_skill, self.bot_creature, self.bot_creature)

    def calculate_damage(self, attacker, skill, defender):
        return max(0, attacker.attack + skill.base_damage - defender.defense)

    def handle_battle_end(self, player_won):
        if player_won:
            self._show_text(self.player, "You won!")
        else:
            self._show_text(self.player, "You lost!")
        self._transition_to_scene("MainMenuScene")
