from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_selected_skill = None
        self.opponent_selected_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_selected_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.opponent_selected_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
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

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _resolve_turn(self):
        # Determine order
        first = self.player
        second = self.opponent
        first_skill = self.player_selected_skill
        second_skill = self.opponent_selected_skill
        first_creature = self.player_creature
        second_creature = self.opponent_creature

        if self.opponent_creature.speed > self.player_creature.speed or \
           (self.opponent_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_skill, second_skill = second_skill, first_skill
            first_creature, second_creature = second_creature, first_creature

        # Execute skills
        self._execute_skill(first_skill, first_creature, second_creature)
        if second_creature.hp > 0:
            self._execute_skill(second_skill, second_creature, first_creature)

    def _execute_skill(self, skill, attacker, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.display_name}")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
