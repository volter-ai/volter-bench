from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player

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
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A battle begins between {self.player.display_name} and {self.opponent.display_name}!")
        
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
            
            # Execute skills
            self._execute_skill(*first)
            if self._check_battle_end():
                break
                
            self._execute_skill(*second)
            if self._check_battle_end():
                break

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_order(self, action1, action2):
        if action1[1].speed > action2[1].speed:
            return action1, action2
        elif action2[1].speed > action1[1].speed:
            return action2, action1
        else:
            import random
            return random.choice([(action1, action2), (action2, action1)])

    def _calculate_damage(self, attacker_creature, skill, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        type_multipliers = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        multiplier = type_multipliers.get((skill.skill_type, defender_creature.creature_type), 1.0)
        return int(raw_damage * multiplier)

    def _execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.opponent
            defender_creature = self.opponent_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        damage = self._calculate_damage(attacker_creature, skill, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}! "
            f"Dealt {damage} damage to {defender.display_name}'s {defender_creature.display_name}!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} has been defeated!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} is victorious!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
