from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            self.player_choice = self._wait_for_choice(
                self.player,
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )
            
            # Opponent choice phase
            self.opponent_choice = self._wait_for_choice(
                self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills]
            )
            
            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(first)
            if self.check_battle_end():
                break
                
            self.execute_move(second)
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.sample([self.player, self.opponent], 2)

    def execute_move(self, attacker):
        if attacker == self.player:
            attacking_creature = self.player_creature
            defending_creature = self.opponent_creature
            skill = self.player_creature.skills[0]  # Using tackle for now
        else:
            attacking_creature = self.opponent_creature
            defending_creature = self.player_creature
            skill = self.opponent_creature.skills[0]  # Using tackle for now

        damage = attacking_creature.attack + skill.base_damage - defending_creature.defense
        defending_creature.hp -= max(1, damage)  # Minimum 1 damage
        
        self._show_text(self.player, 
            f"{attacking_creature.display_name} used {skill.display_name}! "
            f"Dealt {damage} damage to {defending_creature.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
