from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution Phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute moves in order
            for attacker, creature, skill in [first, second]:
                if attacker == self.player:
                    defender = self.opponent
                    target = self.opponent_creature
                else:
                    defender = self.player
                    target = self.player_creature

                damage = self._calculate_damage(creature, target, skill)
                target.hp = max(0, target.hp - damage)
                
                self._show_text(self.player, f"{creature.display_name} used {skill.display_name}! Dealt {damage} damage!")
                self._show_text(self.opponent, f"{creature.display_name} used {skill.display_name}! Dealt {damage} damage!")

                if target.hp <= 0:
                    winner = self.player if target == self.opponent_creature else self.opponent
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._show_text(self.opponent, f"{winner.display_name} wins!")
                    
                    # Reset creatures before leaving - now done directly instead of via method
                    self.player_creature.hp = self.player_creature.max_hp
                    self.opponent_creature.hp = self.opponent_creature.max_hp
                    
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
            return random.choice([(first_pair, second_pair), (second_pair, first_pair)])

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
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
