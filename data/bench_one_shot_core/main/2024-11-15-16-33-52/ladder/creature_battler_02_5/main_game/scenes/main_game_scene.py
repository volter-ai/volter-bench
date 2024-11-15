from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_choice = None
        self.opponent_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_choice = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            
            # Opponent Choice Phase
            self.opponent_choice = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills])
            
            # Resolution Phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(first)
            if self.check_battle_end():
                break
                
            self.execute_move(second)
            if self.check_battle_end():
                break

        self._transition_to_scene("MainMenuScene")

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.sample([self.player, self.opponent], 2)

    def execute_move(self, attacker):
        if attacker == self.player:
            skill = self.player_choice.thing
            attacker_creature = self.player_creature
            defender_creature = self.opponent_creature
        else:
            skill = self.opponent_choice.thing
            attacker_creature = self.opponent_creature
            defender_creature = self.player_creature

        damage = skill.base_damage + attacker_creature.attack - defender_creature.defense
        defender_creature.hp -= max(1, damage)
        
        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
