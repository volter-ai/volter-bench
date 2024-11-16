from mini_game_engine.engine.lib import AbstractGameScene, Button, create_from_game_database
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent choice phase
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute moves in order
            self._execute_skill(*first)
            if self._check_battle_end():
                return
                
            self._execute_skill(*second)
            if self._check_battle_end():
                return

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_order(self, pair1, pair2):
        if pair1[1].speed > pair2[1].speed:
            return pair1, pair2
        elif pair2[1].speed > pair1[1].speed:
            return pair2, pair1
        else:
            return random.sample([pair1, pair2], 2)

    def _calculate_damage(self, attacker, skill, defender):
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
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def _execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender_creature = self.opponent_creature
        else:
            defender_creature = self.player_creature

        damage = self._calculate_damage(attacker_creature, skill, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        
        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name}! "
            f"Dealt {damage} damage to {defender_creature.display_name}")

    def _reset_creatures(self):
        # Reset player's creatures by creating fresh instances from prototypes
        for i, creature in enumerate(self.player.creatures):
            self.player.creatures[i] = create_from_game_database(creature.prototype_id, Creature)
        
        # Reset opponent's creatures
        for i, creature in enumerate(self.opponent.creatures):
            self.opponent.creatures[i] = create_from_game_database(creature.prototype_id, Creature)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._reset_creatures()  # Reset before transitioning
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._reset_creatures()  # Reset before transitioning
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
