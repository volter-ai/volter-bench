from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            player_choice = self._wait_for_choice(
                self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]
            )
            self.player_chosen_skill = player_choice.thing
            
            # Opponent Choice Phase
            opponent_choice = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            )
            self.opponent_chosen_skill = opponent_choice.thing

            # Resolution Phase
            first, second = self.determine_turn_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                break
                
            self.execute_turn(second)
            
            if self.check_battle_end():
                break

    def determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.choice([(self.player, self.opponent), (self.opponent, self.player)])

    def execute_turn(self, acting_player):
        attacker = self.player_creature if acting_player == self.player else self.opponent_creature
        defender = self.opponent_creature if acting_player == self.player else self.player_creature
        skill = self.player_chosen_skill if acting_player == self.player else self.opponent_chosen_skill
        
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp -= max(0, damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
