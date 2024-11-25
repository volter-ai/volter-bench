from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._get_player_choice()
            
            # Opponent choice phase
            opponent_skill = self._get_opponent_choice()
            
            # Resolution phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self._check_battle_end():
                break
        
        # Reset creatures before transitioning
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _reset_creatures(self):
        # Reset all creatures to their max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def _get_player_choice(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(s for s in self.player_creature.skills if s.display_name == choice.display_name)

    def _get_opponent_choice(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(s for s in self.opponent_creature.skills if s.display_name == choice.display_name)

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
        # Determine order
        first, second = self._determine_order(
            (self.player, self.player_creature, player_skill),
            (self.opponent, self.opponent_creature, opponent_skill)
        )
        
        # Execute moves in order
        for attacker, creature, skill in [first, second]:
            if attacker == self.player:
                defender = self.opponent_creature
            else:
                defender = self.player_creature
                
            damage = self._calculate_damage(creature, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(attacker, f"{creature.display_name} used {skill.display_name}!")
            self._show_text(attacker, f"It dealt {damage} damage!")

    def _determine_order(self, player_data, opponent_data):
        p_creature = player_data[1]
        o_creature = opponent_data[1]
        
        if p_creature.speed > o_creature.speed:
            return player_data, opponent_data
        elif p_creature.speed < o_creature.speed:
            return opponent_data, player_data
        else:
            return random.sample([player_data, opponent_data], 2)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
