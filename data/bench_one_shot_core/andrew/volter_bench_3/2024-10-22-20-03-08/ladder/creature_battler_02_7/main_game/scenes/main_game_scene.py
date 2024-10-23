from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        while not self.battle_ended:
            # Player Choice Phase
            player_skill = self.player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            self.battle_ended = self.check_battle_end()

        # After battle ends, show result and return to main menu
        self._show_text(self.player, "Battle Ended!")
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def foe_choice_phase(self, opponent: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in creature.skills]
        choice = self._wait_for_choice(opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature, player_skill, foe_skill)
        
        self.execute_skill(first[0], first[1], second[1], first[2])
        if self.check_battle_end():
            return
        
        self.execute_skill(second[0], second[1], first[1], second[2])

    def determine_order(self, creature1: Creature, creature2: Creature, skill1: Skill, skill2: Skill):
        if creature1.speed > creature2.speed:
            return (self.player, creature1, skill1), (self.opponent, creature2, skill2)
        elif creature2.speed > creature1.speed:
            return (self.opponent, creature2, skill2), (self.player, creature1, skill1)
        else:
            if random.choice([True, False]):
                return (self.player, creature1, skill1), (self.opponent, creature2, skill2)
            else:
                return (self.opponent, creature2, skill2), (self.player, creature1, skill1)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, defender_creature: Creature, skill: Skill):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted. You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted. You win!")
            return True
        return False
