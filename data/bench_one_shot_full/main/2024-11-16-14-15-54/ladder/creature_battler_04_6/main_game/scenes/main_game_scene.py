from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
        # Reset creatures to full HP
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{self._format_skills()}
"""

    def _format_skills(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type effectiveness
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

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(self.opponent, self.opponent_creature.skills)

            # Resolution phase
            first, second = self._determine_turn_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute turns
            for attacker, creature, skill in [first, second]:
                if attacker == self.player:
                    target = self.opponent_creature
                else:
                    target = self.player_creature
                    
                damage = self.calculate_damage(creature, target, skill)
                target.hp = max(0, target.hp - damage)
                
                self._show_text(self.player, f"{creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"Dealt {damage} damage!")

                if target.hp == 0:
                    winner = "You" if attacker == self.player else "Opponent"
                    self._show_text(self.player, f"{winner} won the battle!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _determine_turn_order(self, player_data, opponent_data):
        player_creature = player_data[1]
        opponent_creature = opponent_data[1]
        
        if player_creature.speed > opponent_creature.speed:
            return player_data, opponent_data
        elif player_creature.speed < opponent_creature.speed:
            return opponent_data, player_data
        else:
            return random.choice([(player_data, opponent_data), (opponent_data, player_data)])
