from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self._show_text(self.opponent, f"""=== Opponent's Turn ===
{self.opponent_creature.display_name}'s Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.opponent_creature.skills])}""")
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )
            
            # Execute skills in order
            for attacker, attacker_creature, skill in [first, second]:
                if attacker == self.player:
                    defender = self.opponent
                    defender_creature = self.opponent_creature
                else:
                    defender = self.player
                    defender_creature = self.player_creature
                    
                damage = self._calculate_damage(skill, attacker_creature, defender_creature)
                defender_creature.hp = max(0, defender_creature.hp - damage)
                
                self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
                self._show_text(defender, f"{defender_creature.display_name} took {damage} damage!")
                
                if defender_creature.hp <= 0:
                    if defender == self.player:
                        self._show_text(self.player, "You lost!")
                    else:
                        self._show_text(self.player, "You won!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _determine_order(self, first_pair, second_pair):
        if first_pair[1].speed > second_pair[1].speed:
            return first_pair, second_pair
        elif first_pair[1].speed < second_pair[1].speed:
            return second_pair, first_pair
        else:
            import random
            return random.choice([(first_pair, second_pair), (second_pair, first_pair)])

    def _calculate_damage(self, skill, attacker, defender):
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
