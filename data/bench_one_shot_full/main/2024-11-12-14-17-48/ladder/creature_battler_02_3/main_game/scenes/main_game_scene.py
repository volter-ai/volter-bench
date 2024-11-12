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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
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
            self.execute_move(*first)
            if self.check_battle_end():
                break
                
            self.execute_move(*second)
            if self.check_battle_end():
                break

    def determine_order(self, move1, move2):
        p1, c1, _ = move1
        p2, c2, _ = move2
        if c1.speed > c2.speed:
            return move1, move2
        elif c2.speed > c1.speed:
            return move2, move1
        else:
            return (move1, move2) if random.random() < 0.5 else (move2, move1)

    def execute_move(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.bot
            defender_creature = self.bot_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= max(1, damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")

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
