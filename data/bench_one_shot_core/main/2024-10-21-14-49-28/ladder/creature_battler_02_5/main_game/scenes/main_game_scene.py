from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_skill = None
        self.opponent_skill = None
        self.battle_winner = None

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
        while True:
            # Player Choice Phase
            self.player_skill = self.player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            self.opponent_skill = self.player_choice_phase(self.opponent, self.opponent_creature)

            # Resolution Phase
            self.resolution_phase()

            # Check for battle end
            battle_ended, winner = self.check_battle_end()
            if battle_ended:
                self.battle_winner = winner
                self._transition_to_scene("BattleResultScene")
                return

    def player_choice_phase(self, current_player, current_creature):
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def resolution_phase(self):
        first, second = self.determine_order()
        
        self.execute_skill(*first)
        if self.check_battle_end()[0]:
            return
        
        self.execute_skill(*second)

    def determine_order(self):
        player_tuple = (self.player, self.player_creature, self.player_skill, self.opponent_creature)
        opponent_tuple = (self.opponent, self.opponent_creature, self.opponent_skill, self.player_creature)
        
        if self.player_creature.speed > self.opponent_creature.speed:
            return player_tuple, opponent_tuple
        elif self.opponent_creature.speed > self.player_creature.speed:
            return opponent_tuple, player_tuple
        else:
            return random.choice([(player_tuple, opponent_tuple), (opponent_tuple, player_tuple)])

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted!")
            return True, self.opponent
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted!")
            return True, self.player
        return False, None
