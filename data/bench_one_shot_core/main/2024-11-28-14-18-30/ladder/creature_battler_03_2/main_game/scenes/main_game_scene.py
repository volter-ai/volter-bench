from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} - {skill.base_damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player phase
            self.player_chosen_skill = self._wait_for_choice(
                self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent phase
            self.opponent_chosen_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            if not self.execute_move(first):
                break
            if not self.execute_move(second):
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_chosen_skill), (self.opponent, self.opponent_chosen_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            return (self.opponent, self.opponent_chosen_skill), (self.player, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_chosen_skill), (self.opponent, self.opponent_chosen_skill)
            return (self.opponent, self.opponent_chosen_skill), (self.player, self.player_chosen_skill)

    def execute_move(self, move_tuple):
        attacker, skill = move_tuple
        if attacker == self.player:
            attacking_creature = self.player_creature
            defending_creature = self.opponent_creature
        else:
            attacking_creature = self.opponent_creature
            defending_creature = self.player_creature

        # Calculate damage
        raw_damage = attacking_creature.attack + skill.base_damage - defending_creature.defense
        
        # Type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defending_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defending_creature.hp = max(0, defending_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacking_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")

        # Check for battle end
        if defending_creature.hp <= 0:
            winner = self.player if attacker == self.player else self.opponent
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return False
        return True

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)
