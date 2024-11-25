from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
            player_skill = self._handle_player_turn()
            
            # Foe Choice Phase
            opponent_skill = self._handle_opponent_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self._check_battle_end():
                break

        # Reset creatures before leaving
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _reset_creatures(self):
        """Reset creatures' HP to their max values"""
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def _handle_player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _handle_opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order based on speed
        if self.player_creature.speed == self.opponent_creature.speed:
            # Equal speeds - 50% chance for either to go first
            if random.random() < 0.5:
                first = self.player_creature
                second = self.opponent_creature
                first_skill = player_skill
                second_skill = opponent_skill
            else:
                first = self.opponent_creature
                second = self.player_creature
                first_skill = opponent_skill
                second_skill = player_skill
        else:
            # Different speeds - faster goes first
            first = self.player_creature if self.player_creature.speed > self.opponent_creature.speed else self.opponent_creature
            second = self.opponent_creature if first == self.player_creature else self.player_creature
            first_skill = player_skill if first == self.player_creature else opponent_skill
            second_skill = opponent_skill if first == self.player_creature else player_skill

        # Execute skills in determined order
        if first == self.player_creature:
            damage = self._calculate_damage(first, self.opponent_creature, first_skill)
            self.opponent_creature.hp = max(0, self.opponent_creature.hp - damage)
            self._show_text(self.player, f"Your {first.display_name} used {first_skill.display_name} for {damage} damage!")
            
            if self.opponent_creature.hp > 0:
                damage = self._calculate_damage(second, self.player_creature, second_skill)
                self.player_creature.hp = max(0, self.player_creature.hp - damage)
                self._show_text(self.player, f"Opponent's {second.display_name} used {second_skill.display_name} for {damage} damage!")
        else:
            damage = self._calculate_damage(first, self.player_creature, first_skill)
            self.player_creature.hp = max(0, self.player_creature.hp - damage)
            self._show_text(self.player, f"Opponent's {first.display_name} used {first_skill.display_name} for {damage} damage!")
            
            if self.player_creature.hp > 0:
                damage = self._calculate_damage(second, self.opponent_creature, second_skill)
                self.opponent_creature.hp = max(0, self.opponent_creature.hp - damage)
                self._show_text(self.player, f"Your {second.display_name} used {second_skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
