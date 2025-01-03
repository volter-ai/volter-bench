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
            player_skill = self._handle_player_turn()
            
            # Opponent Choice Phase
            opponent_skill = self._handle_opponent_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                # Instead of breaking, transition back to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def _handle_player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _handle_opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
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
            (self.player_creature, player_skill),
            (self.opponent_creature, opponent_skill)
        )
        
        # Execute skills in order
        for attacker, defender, skill in [first, second]:
            damage = self._calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage to {defender.display_name}!")

    def _determine_order(self, pair1, pair2):
        creature1, skill1 = pair1
        creature2, skill2 = pair2
        
        if creature1.speed > creature2.speed:
            return (creature1, creature2, skill1), (creature2, creature1, skill2)
        elif creature2.speed > creature1.speed:
            return (creature2, creature1, skill2), (creature1, creature2, skill1)
        else:
            if random.random() < 0.5:
                return (creature1, creature2, skill1), (creature2, creature1, skill2)
            return (creature2, creature1, skill2), (creature1, creature2, skill1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
