from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
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
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            self.player_chosen_skill = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent choice phase
            self._show_text(self.opponent, "Choose your skill!")
            self.opponent_chosen_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(*first)
            if self.check_battle_end():
                return
                
            self.execute_move(*second)
            if self.check_battle_end():
                return

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player_creature, self.player_chosen_skill, self.opponent_creature), \
                   (self.opponent_creature, self.opponent_chosen_skill, self.player_creature)
        elif self.opponent_creature.speed > self.player_creature.speed:
            return (self.opponent_creature, self.opponent_chosen_skill, self.player_creature), \
                   (self.player_creature, self.player_chosen_skill, self.opponent_creature)
        else:
            if random.random() < 0.5:
                return (self.player_creature, self.player_chosen_skill, self.opponent_creature), \
                       (self.opponent_creature, self.opponent_chosen_skill, self.player_creature)
            else:
                return (self.opponent_creature, self.opponent_chosen_skill, self.player_creature), \
                       (self.player_creature, self.player_chosen_skill, self.opponent_creature)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def execute_move(self, attacker, skill, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.display_name}!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
