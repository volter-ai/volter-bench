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
            # Show battle state
            self._show_text(self.player, str(self))
            self._show_text(self.opponent, str(self))

            # Player and opponent choose skills
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Determine order
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute skills
            for attacker, creature, skill in [first, second]:
                if attacker == self.player:
                    defender_creature = self.opponent_creature
                else:
                    defender_creature = self.player_creature
                    
                damage = self._calculate_damage(skill, creature, defender_creature)
                defender_creature.hp -= damage
                
                self._show_text(self.player, f"{creature.display_name} used {skill.display_name} for {damage} damage!")
                self._show_text(self.opponent, f"{creature.display_name} used {skill.display_name} for {damage} damage!")

                if defender_creature.hp <= 0:
                    winner = self.player if defender_creature == self.opponent_creature else self.opponent
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._show_text(self.opponent, f"{winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _determine_order(self, p1_data, p2_data):
        p1_player, p1_creature, p1_skill = p1_data
        p2_player, p2_creature, p2_skill = p2_data
        
        if p1_creature.speed > p2_creature.speed:
            return p1_data, p2_data
        elif p2_creature.speed > p1_creature.speed:
            return p2_data, p1_data
        else:
            return random.choice([(p1_data, p2_data), (p2_data, p1_data)])

    def _calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Get type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
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
