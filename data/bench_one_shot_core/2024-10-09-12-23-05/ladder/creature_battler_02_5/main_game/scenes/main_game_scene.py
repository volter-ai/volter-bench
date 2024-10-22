import random

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


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

Player's turn:
{self.get_skill_choices_str(self.player_creature)}
"""

    def get_skill_choices_str(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def player_choice_phase(self) -> Skill:
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self) -> Skill:
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature, player_skill, foe_skill)
        
        self.execute_skill(*first)
        if self.check_battle_end():
            return
        
        self.execute_skill(*second)

    def determine_order(self, creature1: Creature, creature2: Creature, skill1: Skill, skill2: Skill):
        if creature1.speed > creature2.speed:
            return (self.player, self.player_creature, skill1, self.opponent, self.opponent_creature), \
                   (self.opponent, self.opponent_creature, skill2, self.player, self.player_creature)
        elif creature2.speed > creature1.speed:
            return (self.opponent, self.opponent_creature, skill2, self.player, self.player_creature), \
                   (self.player, self.player_creature, skill1, self.opponent, self.opponent_creature)
        else:
            if random.choice([True, False]):
                return (self.player, self.player_creature, skill1, self.opponent, self.opponent_creature), \
                       (self.opponent, self.opponent_creature, skill2, self.player, self.player_creature)
            else:
                return (self.opponent, self.opponent_creature, skill2, self.player, self.player_creature), \
                       (self.player, self.player_creature, skill1, self.opponent, self.opponent_creature)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        defender_creature.hp -= damage
        defender_creature.hp = max(0, defender_creature.hp)  # Ensure HP doesn't go below 0
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
