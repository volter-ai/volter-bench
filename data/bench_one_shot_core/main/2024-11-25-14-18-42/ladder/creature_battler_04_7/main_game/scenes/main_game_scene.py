from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
        # Reset creatures to full HP
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase  
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution Phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute skills in order
            self._execute_skill(*first)
            if self._check_battle_end():
                break

            self._execute_skill(*second)
            if self._check_battle_end():
                break

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _determine_order(self, pair1, pair2):
        player1, creature1, _ = pair1
        player2, creature2, _ = pair2
        
        if creature1.speed > creature2.speed:
            return pair1, pair2
        elif creature2.speed > creature1.speed:
            return pair2, pair1
        else:
            return (pair1, pair2) if random.random() < 0.5 else (pair2, pair1)

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_map = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        return effectiveness_map.get((skill_type, creature_type), 1.0)

    def _execute_skill(self, attacker_player, attacker, skill):
        if attacker_player == self.player:
            defender = self.opponent_creature
        else:
            defender = self.player_creature
            
        damage = self._calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        
        self._show_text(attacker_player, 
            f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
