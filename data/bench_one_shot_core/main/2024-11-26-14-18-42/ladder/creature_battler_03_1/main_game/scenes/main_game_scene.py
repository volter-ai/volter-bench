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
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.opponent_chosen_skill = self._handle_player_turn(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolve_turn()
            
            # Check for battle end
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

    def _resolve_turn(self):
        # Determine order
        first_player, first_skill, second_player, second_skill = self._determine_turn_order()
        
        # Execute skills
        self._execute_skill(first_player, first_skill)
        if second_player.creatures[0].hp > 0:  # Only execute second skill if target still alive
            self._execute_skill(second_player, second_skill)

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.player_chosen_skill, self.opponent, self.opponent_chosen_skill
        elif self.player_creature.speed < self.opponent_creature.speed:
            return self.opponent, self.opponent_chosen_skill, self.player, self.player_chosen_skill
        else:
            if random.random() < 0.5:
                return self.player, self.player_chosen_skill, self.opponent, self.opponent_chosen_skill
            return self.opponent, self.opponent_chosen_skill, self.player, self.player_chosen_skill

    def _execute_skill(self, attacker, skill):
        if attacker == self.player:
            attacking_creature = self.player_creature
            defending_creature = self.opponent_creature
        else:
            attacking_creature = self.opponent_creature
            defending_creature = self.player_creature

        # Calculate raw damage
        raw_damage = attacking_creature.attack + skill.base_damage - defending_creature.defense
        
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defending_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defending_creature.hp = max(0, defending_creature.hp - final_damage)
        
        # Show result
        self._show_text(self.player, 
            f"{attacking_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defending_creature.display_name}")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
