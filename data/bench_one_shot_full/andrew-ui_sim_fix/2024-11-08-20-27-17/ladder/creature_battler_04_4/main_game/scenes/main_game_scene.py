from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

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
            # Player choice phase
            self.player_chosen_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Opponent choice phase
            self.opponent_chosen_skill = self._handle_player_turn(self.opponent, self.opponent_creature)
            
            # Resolution phase
            self._resolve_turn()
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def _handle_player_turn(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self):
        # Determine order
        first_player, first_skill, second_player, second_skill = self._determine_turn_order()
        
        # Execute skills
        self._execute_skill(first_player, first_skill)
        if self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
            self._execute_skill(second_player, second_skill)

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.player_chosen_skill, self.opponent, self.opponent_chosen_skill
        elif self.player_creature.speed < self.opponent_creature.speed:
            return self.opponent, self.opponent_chosen_skill, self.player, self.player_chosen_skill
        else:
            if random.random() < 0.5:
                return self.player, self.player_chosen_skill, self.opponent, self.opponent_chosen_skill
            return self.opponent, self.opponent_chosen_skill, self.player, self.player_chosen_skill

    def _execute_skill(self, attacker, skill):
        attacker_creature = self.player_creature if attacker == self.player else self.opponent_creature
        defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
        
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender_creature.display_name}!")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
