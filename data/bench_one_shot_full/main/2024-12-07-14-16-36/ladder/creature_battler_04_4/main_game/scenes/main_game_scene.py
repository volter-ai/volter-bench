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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase()
            
            # Opponent Choice Phase
            opponent_skill = self._opponent_choice_phase()
            
            # Resolution Phase
            self._resolution_phase(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                break
                
        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        self._show_text(self.player, "Choose your skill!")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_choice_phase(self):
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

    def _resolution_phase(self, player_skill, opponent_skill):
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
            
            self._show_text(self.player, f"{creature.display_name} used {skill.display_name} for {damage} damage!")
            self._show_text(self.opponent, f"{creature.display_name} used {skill.display_name} for {damage} damage!")

    def _determine_order(self, player_tuple, opponent_tuple):
        player_speed = player_tuple[1].speed
        opponent_speed = opponent_tuple[1].speed
        
        if player_speed > opponent_speed:
            return player_tuple, opponent_tuple
        elif opponent_speed > player_speed:
            return opponent_tuple, player_tuple
        else:
            return random.sample([player_tuple, opponent_tuple], 2)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False
