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
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player choice phase
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, choices)
            self.player_chosen_skill = next(s for s in self.player_creature.skills 
                                          if s.display_name == choice.display_name)

            # Opponent choice phase
            opponent_choice = self._wait_for_choice(self.opponent, 
                [Button(skill.display_name) for skill in self.opponent_creature.skills])
            self.opponent_chosen_skill = next(s for s in self.opponent_creature.skills 
                                            if s.display_name == opponent_choice.display_name)

            # Resolution phase
            first, second = self.determine_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                self._quit_whole_game()
                return
                
            self.execute_turn(second)
            
            if self.check_battle_end():
                self._quit_whole_game()
                return

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.choice([(self.player, self.opponent), (self.opponent, self.player)])

    def execute_turn(self, attacker):
        skill = self.player_chosen_skill if attacker == self.player else self.opponent_chosen_skill
        attacker_creature = self.player_creature if attacker == self.player else self.opponent_creature
        defender_creature = self.opponent_creature if attacker == self.player else self.player_creature

        # Calculate damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        type_factor = self.get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name}! Dealt {final_damage} damage!")

    def get_type_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
