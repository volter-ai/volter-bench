from mini_game_engine.engine.lib import AbstractGameScene, Button
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

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills])

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills])

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_turn(first, second)
            
            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.choice([(self.player, self.opponent), (self.opponent, self.player)])

    def execute_turn(self, first, second):
        # Calculate and apply damage
        attacker = first.creatures[0]
        defender = second.creatures[0]
        skill = first.creatures[0].skills[0]
        
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp -= max(0, damage)

        if defender.hp > 0:
            attacker = second.creatures[0]
            defender = first.creatures[0]
            skill = second.creatures[0].skills[0]
            
            damage = attacker.attack + skill.base_damage - defender.defense
            defender.hp -= max(0, damage)
