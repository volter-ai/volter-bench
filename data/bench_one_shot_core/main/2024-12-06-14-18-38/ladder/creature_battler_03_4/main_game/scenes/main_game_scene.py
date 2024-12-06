from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

VS

{self.opponent.display_name}'s {self.opponent_creature.display_name}
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
Type: {self.opponent_creature.creature_type}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player phase
            self._show_text(self.player, "Your turn!")
            player_skill = self._wait_for_choice(
                self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent phase
            self._show_text(self.opponent, "Opponent's turn!")
            opponent_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute skills
            for attacker, creature, skill in [first, second]:
                if attacker == self.player:
                    defender_creature = self.opponent_creature
                else:
                    defender_creature = self.player_creature
                    
                damage = self.calculate_damage(skill, creature, defender_creature)
                defender_creature.hp -= damage
                
                self._show_text(self.player, 
                    f"{creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage to {defender_creature.display_name}!")

                if defender_creature.hp <= 0:
                    defender_creature.hp = 0
                    winner = self.player if attacker == self.player else self.opponent
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def determine_order(self, action1, action2):
        p1_creature = action1[1]
        p2_creature = action2[1]
        
        if p1_creature.speed > p2_creature.speed:
            return action1, action2
        elif p2_creature.speed > p1_creature.speed:
            return action2, action1
        else:
            return (action1, action2) if random.random() < 0.5 else (action2, action1)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Get type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * effectiveness)
        return max(final_damage, 1)  # Minimum 1 damage

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)
