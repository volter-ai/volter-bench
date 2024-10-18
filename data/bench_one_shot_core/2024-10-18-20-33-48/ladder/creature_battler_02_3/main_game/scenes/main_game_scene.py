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
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            player_skill = self.player_turn()
            
            # Foe Choice Phase
            opponent_skill = self.opponent_turn()
            
            # Resolution Phase
            self.resolve_turn(player_skill, opponent_skill)
            
            if self.check_battle_end():
                self.end_battle()
                break

    def player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            first_attacker, first_skill, second_attacker, second_skill = (
                self.player, player_skill, self.opponent, opponent_skill
            )
        elif self.player_creature.speed < self.opponent_creature.speed:
            first_attacker, first_skill, second_attacker, second_skill = (
                self.opponent, opponent_skill, self.player, player_skill
            )
        else:
            # Random order when speeds are equal
            if random.choice([True, False]):
                first_attacker, first_skill, second_attacker, second_skill = (
                    self.player, player_skill, self.opponent, opponent_skill
                )
            else:
                first_attacker, first_skill, second_attacker, second_skill = (
                    self.opponent, opponent_skill, self.player, player_skill
                )

        self.execute_skill(first_attacker, first_attacker.creatures[0], first_skill, second_attacker.creatures[0])
        if second_attacker.creatures[0].hp > 0:
            self.execute_skill(second_attacker, second_attacker.creatures[0], second_skill, first_attacker.creatures[0])

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
        else:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
        
        self._show_text(self.player, "Returning to main menu...")
        self._transition_to_scene("MainMenuScene")
