from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_skills = {}

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            player_skill = self._handle_player_turn()
            
            # Opponent Choice Phase
            opponent_skill = self._handle_opponent_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                break

        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return self.player_creature.skills[choices.index(choice)]

    def _handle_opponent_turn(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return self.opponent_creature.skills[choices.index(choice)]

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
        
        # Execute skills in order
        for attacker, creature, skill in [first, second]:
            if attacker == self.player:
                defender_creature = self.opponent_creature
            else:
                defender_creature = self.player_creature
                
            damage = self._calculate_damage(creature, defender_creature, skill)
            defender_creature.hp = max(0, defender_creature.hp - damage)
            
            self._show_text(self.player, f"{creature.display_name} used {skill.display_name}! Dealt {damage} damage!")
            
            if defender_creature.hp == 0:
                break

    def _determine_order(self, player_data, opponent_data):
        player_speed = player_data[1].speed
        opponent_speed = opponent_data[1].speed
        
        if player_speed > opponent_speed:
            return player_data, opponent_data
        elif opponent_speed > player_speed:
            return opponent_data, player_data
        else:
            return random.sample([player_data, opponent_data], 2)

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
