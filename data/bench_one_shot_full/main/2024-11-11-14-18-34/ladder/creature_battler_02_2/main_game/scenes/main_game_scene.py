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
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self._wait_for_choice(
                self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Bot choice phase
            self.bot_chosen_skill = self._wait_for_choice(
                self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]
            ).thing

            # Resolution phase
            first, second = self.determine_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                break
                
            self.execute_turn(second)
            
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.bot)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.player)
        else:
            return random.choice([(self.player, self.bot), (self.bot, self.player)])

    def execute_turn(self, attacker):
        if attacker == self.player:
            skill = self.player_chosen_skill
            atk_creature = self.player_creature
            def_creature = self.bot_creature
        else:
            skill = self.bot_chosen_skill
            atk_creature = self.bot_creature
            def_creature = self.player_creature

        damage = max(0, skill.base_damage + atk_creature.attack - def_creature.defense)
        def_creature.hp = max(0, def_creature.hp - damage)
        
        self._show_text(self.player, f"{atk_creature.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} was defeated! You lose!")
            self._quit_whole_game()
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} was defeated! You win!")
            self._quit_whole_game()
            return True
        return False
