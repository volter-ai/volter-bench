from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_actions = {}

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player phase
            player_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Opponent phase
            opponent_skill = self._handle_player_turn(self.opponent, self.opponent_creature)
            
            # Resolution phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
        
        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order
        first, second = self._determine_order(
            (self.player, self.player_creature, player_skill),
            (self.opponent, self.opponent_creature, opponent_skill)
        )
        
        # Execute skills
        self._execute_skill(*first)
        if second[1].hp > 0:  # Only execute second if still alive
            self._execute_skill(*second)

    def _determine_order(self, action1, action2):
        if action1[1].speed > action2[1].speed:
            return action1, action2
        elif action2[1].speed > action1[1].speed:
            return action2, action1
        else:
            return random.choice([(action1, action2), (action2, action1)])

    def _execute_skill(self, attacker, attacker_creature, skill):
        defender = self.opponent if attacker == self.player else self.player
        defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        # Show result
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"Dealt {final_damage} damage!")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
