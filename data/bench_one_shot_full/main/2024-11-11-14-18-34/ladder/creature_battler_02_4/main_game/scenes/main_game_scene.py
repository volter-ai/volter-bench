from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            # Player phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Bot phase
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolution phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )

            # Execute moves
            for attacker, creature, skill in [first, second]:
                if attacker == self.player:
                    defender_creature = self.bot_creature
                else:
                    defender_creature = self.player_creature

                damage = self.calculate_damage(creature, defender_creature, skill)
                defender_creature.hp -= damage
                
                self._show_text(self.player, 
                    f"{creature.display_name} used {skill.display_name} for {damage} damage!")

                if defender_creature.hp <= 0:
                    winner = "You" if attacker == self.player else "Bot"
                    self._show_text(self.player, f"{winner} won the battle!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def determine_order(self, p1_data, p2_data):
        p1_creature = p1_data[1]
        p2_creature = p2_data[1]
        
        if p1_creature.speed > p2_creature.speed:
            return p1_data, p2_data
        elif p2_creature.speed > p1_creature.speed:
            return p2_data, p1_data
        else:
            return random.sample([p1_data, p2_data], 2)

    def calculate_damage(self, attacker, defender, skill):
        return max(0, attacker.attack + skill.base_damage - defender.defense)
