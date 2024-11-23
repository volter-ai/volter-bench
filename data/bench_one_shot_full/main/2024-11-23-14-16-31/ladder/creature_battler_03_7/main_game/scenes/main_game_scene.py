from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Opponent choice phase
            self.opponent_chosen_skill = self._handle_player_turn(self.opponent, self.opponent_creature)
            
            # Resolution phase
            self._resolve_turn()
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, current_player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _calculate_damage(self, skill, attacker, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _resolve_turn(self):
        # Determine order based on creature speeds
        if self.opponent_creature.speed > self.player_creature.speed or \
           (self.opponent_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first_creature = self.opponent_creature
            second_creature = self.player_creature
            first_skill = self.opponent_chosen_skill
            second_skill = self.player_chosen_skill
            first_player = self.opponent
            second_player = self.player
        else:
            first_creature = self.player_creature
            second_creature = self.opponent_creature
            first_skill = self.player_chosen_skill
            second_skill = self.opponent_chosen_skill
            first_player = self.player
            second_player = self.opponent

        # Execute skills
        for attacker, defender, skill, attacking_player in [
            (first_creature, second_creature, first_skill, first_player),
            (second_creature, first_creature, second_skill, second_player)
        ]:
            if defender.hp > 0:  # Only attack if defender still alive
                damage = self._calculate_damage(skill, attacker, defender)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(self.player, 
                    f"{attacking_player.display_name}'s {attacker.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage!")
