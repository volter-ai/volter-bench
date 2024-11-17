from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_skill = None
        self.opponent_skill = None

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_skill = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent Choice Phase  
            self.opponent_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution Phase
            first, second = self.determine_order()
            
            # Execute skills
            self.execute_skill(*first)
            if self.check_battle_end():
                break
                
            self.execute_skill(*second)
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_skill, self.opponent_creature), (self.opponent, self.opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_skill, self.player_creature), (self.player, self.player_skill, self.opponent_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_skill, self.opponent_creature), (self.opponent, self.opponent_skill, self.player_creature)
            return (self.opponent, self.opponent_skill, self.player_creature), (self.player, self.player_skill, self.opponent_creature)

    def execute_skill(self, attacker, skill, target):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.creatures[0].attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.creatures[0].sp_attack / target.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self.get_type_factor(skill.skill_type, target.creature_type)
        final_damage = int(factor * raw_damage)
        
        target.hp = max(0, target.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name}'s {skill.display_name} dealt {final_damage} damage!")

    def get_type_factor(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
