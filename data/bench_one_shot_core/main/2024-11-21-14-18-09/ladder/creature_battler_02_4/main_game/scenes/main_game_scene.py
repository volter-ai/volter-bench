from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._handle_player_turn(self.player)
            
            # Opponent Choice Phase
            opponent_skill = self._handle_player_turn(self.opponent)
            
            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()  # Properly end the game when battle is over

    def _handle_player_turn(self, current_player):
        creature = self.player_creature if current_player == self.player else self.opponent_creature
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return creature.skills[choices.index(choice)]

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order based on speed
        first = (self.player_creature, player_skill) if self.player_creature.speed > self.opponent_creature.speed else (self.opponent_creature, opponent_skill)
        second = (self.opponent_creature, opponent_skill) if first[0] == self.player_creature else (self.player_creature, player_skill)
        
        # If speeds are equal, randomize
        if self.player_creature.speed == self.opponent_creature.speed:
            if random.random() < 0.5:
                first, second = second, first

        # Execute skills in order
        self._execute_skill(first[0], first[1], second[0])
        if second[0].hp > 0:  # Only execute second skill if target still alive
            self._execute_skill(second[0], second[1], first[0])

    def _execute_skill(self, attacker, skill, defender):
        damage = attacker.attack + skill.base_damage - defender.defense
        damage = max(0, damage)  # Ensure damage isn't negative
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
