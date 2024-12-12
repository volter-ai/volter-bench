from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, skill_choices)
            self.player_chosen_skill = next(s for s in self.player_creature.skills if s.display_name == choice.display_name)

            # Opponent choice phase
            self._show_text(self.opponent, "Choose your skill!")
            opponent_skill_choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_skill_choices)
            self.opponent_chosen_skill = next(s for s in self.opponent_creature.skills if s.display_name == opponent_choice.display_name)

            # Resolution phase
            self.resolve_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def resolve_turn(self):
        first, second = self.determine_turn_order()
        self.execute_skill(first[0], first[1], first[2], first[3])
        if second[1].hp > 0:  # Only execute second skill if target still alive
            self.execute_skill(second[0], second[1], second[2], second[3])

    def determine_turn_order(self):
        player_data = (self.player, self.opponent_creature, self.player_creature, self.player_chosen_skill)
        opponent_data = (self.opponent, self.player_creature, self.opponent_creature, self.opponent_chosen_skill)
        
        if self.player_creature.speed > self.opponent_creature.speed:
            return player_data, opponent_data
        elif self.player_creature.speed < self.opponent_creature.speed:
            return opponent_data, player_data
        else:
            return random.choice([(player_data, opponent_data), (opponent_data, player_data)])

    def execute_skill(self, attacker, defender_creature, attacker_creature, skill):
        # Calculate raw damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        # Show result
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness}")

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)
