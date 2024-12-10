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
ATK: {self.player_creature.attack} DEF: {self.player_creature.defense} SPD: {self.player_creature.speed}

{self.bot.display_name}'s {self.bot_creature.display_name}:
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
ATK: {self.bot_creature.attack} DEF: {self.bot_creature.defense} SPD: {self.bot_creature.speed}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills])

            # Bot choice phase
            bot_skill = self._wait_for_choice(self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills])

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
        # Calculate and apply damage
        if first == self.player:
            attacker, defender = self.player_creature, self.bot_creature
        else:
            attacker, defender = self.bot_creature, self.player_creature
            
        damage = attacker.attack + attacker.skills[0].base_damage - defender.defense
        defender.hp -= max(0, damage)

        if defender.hp > 0:
            if second == self.player:
                attacker, defender = self.player_creature, self.bot_creature
            else:
                attacker, defender = self.bot_creature, self.player_creature
                
            damage = attacker.attack + attacker.skills[0].base_damage - defender.defense
            defender.hp -= max(0, damage)
