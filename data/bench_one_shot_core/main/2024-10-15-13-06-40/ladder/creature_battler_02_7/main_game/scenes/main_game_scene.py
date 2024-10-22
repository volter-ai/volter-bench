from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
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

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
> Quit
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            # Player Choice Phase
            player_choice = self.player_choice_phase()
            
            if isinstance(player_choice, Button) and player_choice.display_name == "Quit":
                self._quit_whole_game()
                return

            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase(player_choice.thing, foe_skill)

            # Check for battle end
            if self.check_battle_end():
                return

    def player_choice_phase(self):
        skill_choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        quit_choice = Button("Quit")
        choices = skill_choices + [quit_choice]
        return self._wait_for_choice(self.player, choices)

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        if self.player_creature.speed == self.opponent_creature.speed:
            # If speeds are equal, randomly choose who goes first
            first_attacker, second_attacker = random.choice([
                (self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature, foe_skill),
                (self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature, player_skill)
            ])
        elif self.player_creature.speed > self.opponent_creature.speed:
            first_attacker = (self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature, foe_skill)
            second_attacker = (self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature, player_skill)
        else:
            first_attacker = (self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature, player_skill)
            second_attacker = (self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature, foe_skill)

        # Execute skills in the determined order
        self.execute_skill(*first_attacker[:3], first_attacker[4])
        if first_attacker[4].hp > 0:
            self.execute_skill(*second_attacker[:3], second_attacker[4])

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
