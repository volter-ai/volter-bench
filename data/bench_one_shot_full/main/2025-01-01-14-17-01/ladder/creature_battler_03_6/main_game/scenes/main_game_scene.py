from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""=== Main Game ===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}

Your Creature: {self.player.creatures[0].display_name} (HP: {self.player.creatures[0].hp})
Opponent Creature: {self.opponent.creatures[0].display_name} (HP: {self.opponent.creatures[0].hp})

Choose a skill:
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self.player_choice_phase()
            if self.opponent.creatures[0].hp <= 0:
                self._show_text(self.player, "You win!")
                self._quit_whole_game()
                return
            self.foe_choice_phase()
            if self.player.creatures[0].hp <= 0:
                self._show_text(self.player, "You lose!")
                self._quit_whole_game()
                return
            self.resolution_phase()

    def player_choice_phase(self):
        creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = choice.thing

    def foe_choice_phase(self):
        creature = self.opponent.creatures[0]
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill = choice.thing

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Calculate damage
        player_damage = self.calculate_damage(self.player_skill, player_creature, opponent_creature)
        opponent_damage = self.calculate_damage(self.opponent_skill, opponent_creature, player_creature)

        # Apply damage
        opponent_creature.hp -= player_damage
        player_creature.hp -= opponent_damage

    def calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        factor = self.get_weakness_resistance_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * factor)
        return max(final_damage, 0)

    def get_weakness_resistance_factor(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)
