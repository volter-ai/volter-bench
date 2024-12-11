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
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.player_chosen_skill = next(s for s in self.player_creature.skills 
                                         if s.display_name == player_choice.display_name)

            # Opponent choice phase
            self._show_text(self.opponent, "Choose your skill!")
            opponent_skill_choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_skill_choices)
            self.opponent_chosen_skill = next(s for s in self.opponent_creature.skills 
                                           if s.display_name == opponent_choice.display_name)

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(*first)
            if self.check_battle_end():
                break
                
            self.execute_move(*second)
            if self.check_battle_end():
                break

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
        # Calculate raw damage
        raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        
        # Apply type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Ensure minimum 1 damage
        final_damage = max(1, final_damage)
        
        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name} used {skill.display_name} on {defender.display_name} for {final_damage} damage!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} wins!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
