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
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")

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

                self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")
                self._show_text(self.opponent, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

                if defender_creature.hp <= 0:
                    winner = attacker
                    self._show_text(self.player, f"{'You won!' if winner == self.player else 'You lost!'}")
                    self._show_text(self.opponent, f"{'You won!' if winner == self.opponent else 'You lost!'}")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _determine_order(self, player_data, opponent_data):
        player_creature = player_data[1]
        opponent_creature = opponent_data[1]
        
        if player_creature.speed > opponent_creature.speed:
            return player_data, opponent_data
        elif player_creature.speed < opponent_creature.speed:
            return opponent_data, player_data
        else:
            return random.choice([(player_data, opponent_data), (opponent_data, player_data)])

    def _calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
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
