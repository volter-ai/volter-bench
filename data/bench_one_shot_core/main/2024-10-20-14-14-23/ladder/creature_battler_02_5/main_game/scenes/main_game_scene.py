from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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
        self.game_loop()

    def game_loop(self):
        battle_ended = False
        while not battle_ended:
            # Player Choice Phase
            player_skill = self.player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            opponent_skill = self.foe_choice_phase(self.opponent, self.opponent_creature)

            # Resolution Phase
            self.resolution_phase(player_skill, opponent_skill)

            # Check for battle end condition
            battle_ended = self.check_battle_end()

        # End the game when the battle is over
        self._quit_whole_game()

    def player_choice_phase(self, player, creature):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def foe_choice_phase(self, opponent, creature):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in creature.skills]
        choice = self._wait_for_choice(opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, opponent_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature, player_skill, opponent_skill)
        
        self.execute_skill(first[0], first[1], second[1], first[2])
        if self.check_battle_end():
            return
        
        self.execute_skill(second[0], second[1], first[1], second[2])

    def determine_order(self, creature1, creature2, skill1, skill2):
        if creature1.speed > creature2.speed:
            return (self.player, creature1, skill1), (self.opponent, creature2, skill2)
        elif creature2.speed > creature1.speed:
            return (self.opponent, creature2, skill2), (self.player, creature1, skill1)
        else:
            if random.choice([True, False]):
                return (self.player, creature1, skill1), (self.opponent, creature2, skill2)
            else:
                return (self.opponent, creature2, skill2), (self.player, creature1, skill1)

    def execute_skill(self, attacker, attacker_creature, defender_creature, skill):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender_creature.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} has been defeated. You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} has been defeated. You win!")
            return True
        return False
