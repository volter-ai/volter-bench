from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            
            # Opponent Choice Phase
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills])

            # Resolution Phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill.thing),
                (self.opponent, self.opponent_creature, opponent_skill.thing)
            )

            # Execute moves in order
            for attacker, creature, skill in [first, second]:
                if attacker == self.player:
                    defender_creature = self.opponent_creature
                else:
                    defender_creature = self.player_creature
                    
                damage = self._calculate_damage(skill, creature, defender_creature)
                defender_creature.hp -= damage
                
                self._show_text(self.player, 
                    f"{creature.display_name} used {skill.display_name}! Dealt {damage} damage!")
                
                if defender_creature.hp <= 0:
                    defender_creature.hp = 0
                    winner = self.player if attacker == self.player else self.opponent
                    self._show_text(self.player, 
                        f"{defender_creature.display_name} fainted! {winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _determine_order(self, p1_tuple, p2_tuple):
        p1_player, p1_creature, p1_skill = p1_tuple
        p2_player, p2_creature, p2_skill = p2_tuple
        
        if p1_creature.speed > p2_creature.speed:
            return p1_tuple, p2_tuple
        elif p2_creature.speed > p1_creature.speed:
            return p2_tuple, p1_tuple
        else:
            return (p1_tuple, p2_tuple) if random.random() < 0.5 else (p2_tuple, p1_tuple)

    def _calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        raw_damage = skill.base_damage + attacker.attack - defender.defense
        
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        return max(1, final_damage)  # Minimum 1 damage

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
