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
        self._show_text(self.opponent, "Battle Start!")

        while True:
            # Player Choice Phase
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_chosen_skill = self._wait_for_choice(self.player, skill_choices).thing

            # Opponent Choice Phase
            opponent_skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
            self.opponent_chosen_skill = self._wait_for_choice(self.opponent, opponent_skill_choices).thing

            # Resolution Phase
            first, second = self.determine_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                break
                
            self.execute_turn(second)
            
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_chosen_skill), (self.opponent, self.opponent_chosen_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            return (self.opponent, self.opponent_chosen_skill), (self.player, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_chosen_skill), (self.opponent, self.opponent_chosen_skill)
            return (self.opponent, self.opponent_chosen_skill), (self.player, self.player_chosen_skill)

    def execute_turn(self, turn):
        attacker, skill = turn
        if attacker == self.player:
            attacking_creature = self.player_creature
            defending_creature = self.opponent_creature
        else:
            attacking_creature = self.opponent_creature
            defending_creature = self.player_creature

        damage = attacking_creature.attack + skill.base_damage - defending_creature.defense
        defending_creature.hp -= max(0, damage)

        self._show_text(self.player, f"{attacking_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacking_creature.display_name} used {skill.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.opponent, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.opponent, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
