from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Bot Choice Phase
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolution Phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )

            # Execute skills
            self.execute_skill(*first)
            if self.check_battle_end():
                break

            if self.bot_creature.hp > 0:
                self.execute_skill(*second)
                if self.check_battle_end():
                    break

    def determine_order(self, action1, action2):
        if action1[1].speed > action2[1].speed:
            return action1, action2
        elif action2[1].speed > action1[1].speed:
            return action2, action1
        else:
            return random.choice([(action1, action2), (action2, action1)])

    def execute_skill(self, attacker, attacker_creature, skill):
        if isinstance(attacker, self.player.__class__):
            defender_creature = self.bot_creature
        else:
            defender_creature = self.player_creature

        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= max(1, damage)
        
        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name}! Dealt {damage} damage!")

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
