from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Opponent Choice Phase  
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Resolution Phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute skills in order
            for attacker, creature, skill in [first, second]:
                if self._execute_skill(attacker, creature, skill):
                    return

            self._show_text(self.player, f"Turn complete!")

    def _determine_order(self, pair1, pair2):
        p1_speed = pair1[1].speed
        p2_speed = pair2[1].speed
        
        if p1_speed > p2_speed:
            return pair1, pair2
        elif p2_speed > p1_speed:
            return pair2, pair1
        else:
            return random.sample([pair1, pair2], 2)

    def _execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.opponent
            defender_creature = self.opponent_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * factor)

        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, 
            f"{attacker_creature.display_name} used {skill.display_name}! Dealt {final_damage} damage!")

        # Check for battle end
        if defender_creature.hp <= 0:
            if defender == self.opponent:
                self._show_text(self.player, "You won!")
            else:
                self._show_text(self.player, "You lost!")
            
            # Reset creatures before transitioning by setting hp back to max_hp
            self.player_creature.hp = self.player_creature.max_hp
            self.opponent_creature.hp = self.opponent_creature.max_hp
            
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False

    def _get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
