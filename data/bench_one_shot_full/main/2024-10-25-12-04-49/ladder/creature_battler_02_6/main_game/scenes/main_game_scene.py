from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild opponent appears!")
        battle_ended = False
        while not battle_ended:
            player_skill = self.player_choice_phase()
            opponent_skill = self.foe_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)
            
            battle_ended = self.check_battle_end()

        # Show the final result and wait for a moment
        self._show_text(self.player, "Battle has ended. Returning to main menu...")
        
        # Transition back to the MainMenuScene
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        self._show_text(self.player, "Choose a skill:")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        return self._wait_for_choice(self.player, choices).thing

    def foe_choice_phase(self):
        return self._wait_for_choice(self.opponent, [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

    def resolution_phase(self, player_skill, opponent_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        self.execute_skill(first, second, first_skill)
        if second.hp > 0:
            self.execute_skill(second, first, second_skill)

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def execute_skill(self, attacker, defender, skill):
        damage = max(0, attacker.attack + skill.base_damage - defender.defense)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name}! {defender.display_name} takes {damage} damage.")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted. You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted. You win!")
            return True
        return False
