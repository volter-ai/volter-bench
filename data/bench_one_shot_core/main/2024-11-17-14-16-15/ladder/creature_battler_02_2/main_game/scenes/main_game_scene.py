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
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

{self.bot.display_name}'s {self.bot_creature.display_name}:
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Attack: {self.bot_creature.attack}
Defense: {self.bot_creature.defense}
Speed: {self.bot_creature.speed}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Your turn!")
            self.player_choice = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )

            # Bot choice phase
            self._show_text(self.bot, "Bot's turn!")
            self.bot_choice = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )

            # Resolution phase
            if self.player_creature.speed > self.bot_creature.speed:
                self.resolve_attack(self.player_creature, self.bot_creature)
                if self.check_win(): return
                self.resolve_attack(self.bot_creature, self.player_creature)
                if self.check_win(): return
            elif self.player_creature.speed < self.bot_creature.speed:
                self.resolve_attack(self.bot_creature, self.player_creature)
                if self.check_win(): return
                self.resolve_attack(self.player_creature, self.bot_creature)
                if self.check_win(): return
            else:
                if random.random() < 0.5:
                    self.resolve_attack(self.player_creature, self.bot_creature)
                    if self.check_win(): return
                    self.resolve_attack(self.bot_creature, self.player_creature)
                    if self.check_win(): return
                else:
                    self.resolve_attack(self.bot_creature, self.player_creature)
                    if self.check_win(): return
                    self.resolve_attack(self.player_creature, self.bot_creature)
                    if self.check_win(): return

    def resolve_attack(self, attacker, defender):
        skill = attacker.skills[0]  # Only tackle for now
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp -= max(0, damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def check_win(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
