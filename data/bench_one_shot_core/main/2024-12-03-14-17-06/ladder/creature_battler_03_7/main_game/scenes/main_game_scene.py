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
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._handle_player_turn()
            
            # Opponent Choice Phase
            opponent_skill = self._handle_opponent_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()  # <-- Added proper game end

    def _handle_player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills 
                   if skill.display_name == choice.display_name)

    def _handle_opponent_turn(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills 
                   if skill.display_name == choice.display_name)

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        type_multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": type_multiplier = 2.0
            elif defender.creature_type == "water": type_multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": type_multiplier = 2.0
            elif defender.creature_type == "leaf": type_multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": type_multiplier = 2.0
            elif defender.creature_type == "fire": type_multiplier = 0.5
            
        return int(raw_damage * type_multiplier)

    def _resolve_turn(self, player_skill, opponent_skill):
        first, second = (self.player_creature, player_skill), (self.opponent_creature, opponent_skill)
        
        if self.opponent_creature.speed > self.player_creature.speed:
            first, second = second, first
        elif self.opponent_creature.speed == self.player_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                
        # First attack
        attacker, skill = first
        defender = self.opponent_creature if attacker == self.player_creature else self.player_creature
        damage = self._calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
        
        if defender.hp > 0:
            # Second attack
            attacker, skill = second
            defender = self.opponent_creature if attacker == self.player_creature else self.player_creature
            damage = self._calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            return True
        return False
