from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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
            
            # Execute skills
            for attacker, attacker_creature, skill in [first, second]:
                if attacker == self.player:
                    defender_creature = self.opponent_creature
                else:
                    defender_creature = self.player_creature
                    
                damage = self._calculate_damage(attacker_creature, defender_creature, skill)
                defender_creature.hp -= damage
                
                self._show_text(self.player, 
                    f"{attacker_creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage to {defender_creature.display_name}!")
                
                if defender_creature.hp <= 0:
                    defender_creature.hp = 0
                    winner = "You" if attacker == self.player else "Opponent"
                    self._show_text(self.player, f"{winner} won the battle!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return creature.skills[0]  # Since we only have tackle for now

    def _determine_order(self, player_data, opponent_data):
        player_creature = player_data[1]
        opponent_creature = opponent_data[1]
        
        if player_creature.speed > opponent_creature.speed:
            return player_data, opponent_data
        elif player_creature.speed < opponent_creature.speed:
            return opponent_data, player_data
        else:
            return random.choice([(player_data, opponent_data), (opponent_data, player_data)])

    def _calculate_damage(self, attacker, defender, skill):
        return max(0, attacker.attack + skill.base_damage - defender.defense)
