from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle Scene===
Player: {self.player_creature.display_name} (HP: {self.player_creature.hp})
Opponent: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp})

Choose your action:
"""

    def run(self):
        while self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
            self.execute_turn()

        # Determine the winner and show the result
        if self.player_creature.hp > 0:
            self._show_text(self.player, "You win!")
        else:
            self._show_text(self.player, "You lose!")

        # Reset the state of the player's creatures
        self.reset_creature_states()

        # Quit the game after the battle
        self._quit_whole_game()

    def execute_turn(self):
        # Player chooses a skill
        player_choice = self.player_turn()

        # Opponent chooses a skill
        opponent_choice = self.opponent_turn()

        # Determine execution order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            self.resolve_skill(self.player_creature, self.opponent_creature, player_choice)
            if self.opponent_creature.hp > 0:
                self.resolve_skill(self.opponent_creature, self.player_creature, opponent_choice)
        elif self.opponent_creature.speed > self.player_creature.speed:
            self.resolve_skill(self.opponent_creature, self.player_creature, opponent_choice)
            if self.player_creature.hp > 0:
                self.resolve_skill(self.player_creature, self.opponent_creature, player_choice)
        else:
            # Random tie-breaker
            if random.choice([True, False]):
                self.resolve_skill(self.player_creature, self.opponent_creature, player_choice)
                if self.opponent_creature.hp > 0:
                    self.resolve_skill(self.opponent_creature, self.player_creature, opponent_choice)
            else:
                self.resolve_skill(self.opponent_creature, self.player_creature, opponent_choice)
                if self.player_creature.hp > 0:
                    self.resolve_skill(self.player_creature, self.opponent_creature, player_choice)

    def player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def resolve_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.calculate_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * effectiveness)
        defender.hp = max(defender.hp - final_damage, 0)

    def calculate_effectiveness(self, skill_type: str, creature_type: str) -> float:
        effectiveness_chart = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)

    def reset_creature_states(self):
        # Reset player's creature state
        self.player_creature.hp = self.player_creature.max_hp
        # Reset opponent's creature state
        self.opponent_creature.hp = self.opponent_creature.max_hp
