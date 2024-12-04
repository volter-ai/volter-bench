from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Resolution phase - create battle tuples
            player_tuple = (self.player, self.player_creature, player_skill)
            opponent_tuple = (self.opponent, self.opponent_creature, opponent_skill)
            
            first, second = self.determine_order(player_tuple, opponent_tuple)

            # Execute moves
            for attacker_tuple in [first, second]:
                # Unpack the tuples properly
                attacker_player, attacker_creature, attack_skill = attacker_tuple
                # The defender is whichever tuple isn't the attacker
                defender_tuple = opponent_tuple if attacker_tuple == player_tuple else player_tuple
                defender_player, defender_creature, _ = defender_tuple

                if defender_creature.hp <= 0:
                    continue
                    
                damage = self.calculate_damage(attacker_creature, defender_creature, attack_skill)
                defender_creature.hp -= damage
                self._show_text(attacker_player, 
                    f"{attacker_creature.display_name} used {attack_skill.display_name} for {damage} damage!")

                if defender_creature.hp <= 0:
                    self._show_text(self.player, 
                        f"{attacker_player.display_name} wins! {defender_creature.display_name} was defeated!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def determine_order(self, player_tuple, opponent_tuple):
        """Takes two tuples of (player, creature, skill) and returns them in speed order"""
        if player_tuple[1].speed > opponent_tuple[1].speed:
            return player_tuple, opponent_tuple
        elif player_tuple[1].speed < opponent_tuple[1].speed:
            return opponent_tuple, player_tuple
        else:
            return random.sample([player_tuple, opponent_tuple], 2)

    def calculate_damage(self, attacker, defender, skill):
        return max(0, attacker.attack + skill.base_damage - defender.defense)
