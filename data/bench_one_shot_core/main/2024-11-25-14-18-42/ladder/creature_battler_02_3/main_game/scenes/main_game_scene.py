from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_actions = []

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
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            
            # Opponent choice phase
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills])

            # Resolution phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill.thing),
                (self.opponent, self.opponent_creature, opponent_skill.thing)
            )

            # Execute skills
            for attacker, creature, skill in [first, second]:
                if creature.hp <= 0:
                    continue
                    
                target = self.opponent_creature if attacker == self.player else self.player_creature
                damage = skill.base_damage + creature.attack - target.defense
                target.hp -= max(1, damage)  # Minimum 1 damage
                
                self._show_text(self.player, 
                    f"{creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage to {target.display_name}!")

                if target.hp <= 0:
                    winner = self.player if attacker == self.player else self.opponent
                    self._show_text(self.player, 
                        f"{winner.display_name} wins! {target.display_name} was defeated!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def determine_order(self, action1, action2):
        p1_creature = action1[1]
        p2_creature = action2[1]
        
        if p1_creature.speed > p2_creature.speed:
            return action1, action2
        elif p1_creature.speed < p2_creature.speed:
            return action2, action1
        else:
            return (action1, action2) if random.random() < 0.5 else (action2, action1)
