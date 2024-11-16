from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self._wait_for_choice(
                self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent choice phase
            self.opponent_chosen_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(first[0], first[1], first[2], first[3])
            if self.check_battle_end():
                break
                
            self.execute_move(second[0], second[1], second[2], second[3])
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill), \
                   (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill), \
                   (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill), \
                       (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill)
            else:
                return (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill), \
                       (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill)

    def execute_move(self, attacker, attacker_creature, defender_creature, skill):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= damage
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            self._quit_whole_game()
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            self._quit_whole_game()
            return True
        return False
