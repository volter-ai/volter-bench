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
        battle_start_text = f"Battle Start! {self.player.display_name} vs {self.bot.display_name}"
        self._show_text(self.player, battle_start_text)
        self._show_text(self.bot, battle_start_text)
        
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
                    defender = self.bot
                    defender_creature = self.bot_creature
                else:
                    defender = self.player
                    defender_creature = self.player_creature
                    
                damage = skill.base_damage + creature.attack - defender_creature.defense
                defender_creature.hp -= max(1, damage)
                
                attack_text = f"{creature.display_name} used {skill.display_name}!"
                damage_text = f"{defender_creature.display_name} took {damage} damage!"
                
                # Show messages to both players
                self._show_text(attacker, attack_text)
                self._show_text(defender, attack_text)
                self._show_text(attacker, damage_text)
                self._show_text(defender, damage_text)
                
                if defender_creature.hp <= 0:
                    if defender_creature == self.player_creature:
                        result_text = "You lost!"
                        self._show_text(self.player, result_text)
                        self._show_text(self.bot, "You won!")
                    else:
                        result_text = "You won!"
                        self._show_text(self.player, result_text)
                        self._show_text(self.bot, "You lost!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def determine_order(self, move1, move2):
        p1_creature = move1[1]
        p2_creature = move2[1]
        
        if p1_creature.speed > p2_creature.speed:
            return move1, move2
        elif p2_creature.speed > p1_creature.speed:
            return move2, move1
        else:
            return random.choice([(move1, move2), (move2, move1)])
