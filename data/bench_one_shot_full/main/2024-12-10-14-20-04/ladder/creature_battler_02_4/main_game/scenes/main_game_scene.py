from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, f"A {self.bot_creature.display_name} appears!")
        
        while True:
            # Player choice phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot choice phase
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )
            
            # Execute moves in order
            for attacker, creature, skill in [first, second]:
                defender_creature = self.bot_creature if attacker == self.player else self.player_creature
                damage = self._calculate_damage(creature, defender_creature, skill)
                defender_creature.hp -= damage
                
                self._show_text(self.player, f"{creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"Dealt {damage} damage!")
                
                if defender_creature.hp <= 0:
                    defender_creature.hp = 0
                    winner = "You" if attacker == self.player else "Opponent"
                    self._show_text(self.player, f"{winner} won the battle!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _determine_order(self, player_data, bot_data):
        player_creature = player_data[1]
        bot_creature = bot_data[1]
        
        if player_creature.speed > bot_creature.speed:
            return player_data, bot_data
        elif bot_creature.speed > player_creature.speed:
            return bot_data, player_data
        else:
            return random.choice([(player_data, bot_data), (bot_data, player_data)])

    def _calculate_damage(self, attacker, defender, skill):
        return max(0, attacker.attack + skill.base_damage - defender.defense)
