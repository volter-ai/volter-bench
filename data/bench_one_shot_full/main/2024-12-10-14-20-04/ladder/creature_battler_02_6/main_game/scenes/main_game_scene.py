from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

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
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )
            
            # Bot choice phase
            bot_skill = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_turn(first, second)
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.bot)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.player)
        else:
            return random.choice([(self.player, self.bot), (self.bot, self.player)])

    def execute_turn(self, first, second):
        # First attacker
        damage = first.creatures[0].attack + first.creatures[0].skills[0].base_damage - second.creatures[0].defense
        second.creatures[0].hp -= max(0, damage)
        self._show_text(self.player, f"{first.creatures[0].display_name} deals {damage} damage!")

        if second.creatures[0].hp > 0:
            # Second attacker
            damage = second.creatures[0].attack + second.creatures[0].skills[0].base_damage - first.creatures[0].defense
            first.creatures[0].hp -= max(0, damage)
            self._show_text(self.player, f"{second.creatures[0].display_name} deals {damage} damage!")
