from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

{self.opponent.display_name}'s {self.opponent_creature.display_name}:
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
Attack: {self.opponent_creature.attack}
Defense: {self.opponent_creature.defense}
Speed: {self.opponent_creature.speed}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player choice phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent choice phase
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )
            
            # Execute moves in order
            for attacker, creature, skill in [first, second]:
                defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
                damage = self._calculate_damage(creature, defender_creature, skill)
                defender_creature.hp -= damage
                
                self._show_text(self.player, f"{creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")
                
                if defender_creature.hp <= 0:
                    defender_creature.hp = 0
                    winner = self.player if defender_creature == self.opponent_creature else self.opponent
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _determine_order(self, first_pair, second_pair):
        first_creature = first_pair[1]
        second_creature = second_pair[1]
        
        if first_creature.speed > second_creature.speed:
            return first_pair, second_pair
        elif second_creature.speed > first_creature.speed:
            return second_pair, first_pair
        else:
            return random.choice([(first_pair, second_pair), (second_pair, first_pair)])

    def _calculate_damage(self, attacker, defender, skill):
        return max(0, attacker.attack + skill.base_damage - defender.defense)
