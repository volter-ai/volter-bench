from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            player_skill = self.choose_skill(self.player, self.player_creature)
            
            # Foe Choice Phase
            opponent_skill = self.choose_skill(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            first, second = self.determine_order(self.player_creature, self.opponent_creature)
            
            self.execute_skill(first[0], first[1], second[1])
            if self.check_battle_end():
                break
            
            self.execute_skill(second[0], second[1], first[1])
            if self.check_battle_end():
                break

    def choose_skill(self, player: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def determine_order(self, creature1: Creature, creature2: Creature):
        if creature1.speed > creature2.speed:
            return (self.player, creature1), (self.opponent, creature2)
        elif creature2.speed > creature1.speed:
            return (self.opponent, creature2), (self.player, creature1)
        else:
            if random.choice([True, False]):
                return (self.player, creature1), (self.opponent, creature2)
            else:
                return (self.opponent, creature2), (self.player, creature1)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, defender_creature: Creature):
        skill = self.choose_skill(attacker, attacker_creature)
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(0, damage)  # Ensure damage is not negative
        defender_creature.hp -= damage
        defender_creature.hp = max(0, defender_creature.hp)  # Ensure HP is not negative
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
