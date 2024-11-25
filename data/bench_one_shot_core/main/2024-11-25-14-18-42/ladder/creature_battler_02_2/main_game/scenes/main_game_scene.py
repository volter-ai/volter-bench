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
            if self.player_creature.speed > self.opponent_creature.speed:
                first, second = self.player, self.opponent
            elif self.player_creature.speed < self.opponent_creature.speed:
                first, second = self.opponent, self.player
            else:
                first, second = random.choice([(self.player, self.opponent), (self.opponent, self.player)])

            # Execute skills
            if first == self.player:
                self._execute_skill(self.player_creature, self.opponent_creature)
                if self.opponent_creature.hp <= 0:
                    self._show_text(self.player, "You win!")
                    self._quit_whole_game()
                self._execute_skill(self.opponent_creature, self.player_creature)
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lose!")
                    self._quit_whole_game()
            else:
                self._execute_skill(self.opponent_creature, self.player_creature)
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lose!")
                    self._quit_whole_game()
                self._execute_skill(self.player_creature, self.opponent_creature)
                if self.opponent_creature.hp <= 0:
                    self._show_text(self.player, "You win!")
                    self._quit_whole_game()

    def _execute_skill(self, attacker, defender):
        skill = attacker.skills[0]  # For now just use tackle
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp -= damage
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {damage} damage!")
