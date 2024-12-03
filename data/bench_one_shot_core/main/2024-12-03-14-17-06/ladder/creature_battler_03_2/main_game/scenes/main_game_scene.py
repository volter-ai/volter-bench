from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.opponent_chosen_skill = self._handle_player_turn(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolve_turn()
            
            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
        
        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _resolve_turn(self):
        # Create battle info tuples without player objects
        player_info = (self.player_creature, self.player_chosen_skill)
        opponent_info = (self.opponent_creature, self.opponent_chosen_skill)

        # Determine order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player, *player_info)
            second = (self.opponent, *opponent_info)
        elif self.opponent_creature.speed > self.player_creature.speed:
            first = (self.opponent, *opponent_info)
            second = (self.player, *player_info)
        else:
            if random.random() < 0.5:
                first = (self.player, *player_info)
                second = (self.opponent, *opponent_info)
            else:
                first = (self.opponent, *opponent_info)
                second = (self.player, *player_info)

        # Execute moves in order
        self._execute_skill(first[0], first[1], first[2], second[1])
        if second[1].hp > 0:  # Only execute second move if target still alive
            self._execute_skill(second[0], second[1], second[2], first[1])

    def _execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        # Calculate raw damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        # Show result
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness}")
        self._show_text(self.player, f"Dealt {final_damage} damage!")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
