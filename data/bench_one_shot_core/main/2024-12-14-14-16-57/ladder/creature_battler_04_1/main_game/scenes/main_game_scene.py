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
            # Player choice phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent choice phase
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute skills
            for attacker, creature, skill in [first, second]:
                if creature.hp <= 0:
                    continue
                    
                target = self.opponent_creature if attacker == self.player else self.player_creature
                damage = self._calculate_damage(creature, target, skill)
                target.hp -= damage
                
                self._show_text(self.player, f"{creature.display_name} used {skill.display_name} for {damage} damage!")
                self._show_text(self.opponent, f"{creature.display_name} used {skill.display_name} for {damage} damage!")

                if target.hp <= 0:
                    winner = self.player if target == self.opponent_creature else self.opponent
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._show_text(self.opponent, f"{winner.display_name} wins!")
                    
                    # Reset creatures before leaving - now done directly
                    self.player_creature.hp = self.player_creature.max_hp
                    self.opponent_creature.hp = self.opponent_creature.max_hp
                    
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_order(self, player_data, opponent_data):
        player_speed = player_data[1].speed
        opponent_speed = opponent_data[1].speed
        
        if player_speed > opponent_speed:
            return player_data, opponent_data
        elif opponent_speed > player_speed:
            return opponent_data, player_data
        else:
            return random.sample([player_data, opponent_data], 2)

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)
