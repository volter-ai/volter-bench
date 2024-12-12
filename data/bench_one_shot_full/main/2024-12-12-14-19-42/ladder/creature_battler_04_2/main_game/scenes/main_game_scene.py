from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.phase = "player_choice"
        self.player_skill = None
        self.opponent_skill = None
        
    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

Phase: {self.phase}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf": multiplier = 2.0
            elif defender_creature.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire": multiplier = 2.0
            elif defender_creature.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water": multiplier = 2.0
            elif defender_creature.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def execute_turn(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine order
        first = player_creature if player_creature.speed > opponent_creature.speed else opponent_creature
        if player_creature.speed == opponent_creature.speed:
            first = random.choice([player_creature, opponent_creature])

        if first == player_creature:
            order = [(player_creature, opponent_creature, self.player_skill),
                    (opponent_creature, player_creature, self.opponent_skill)]
        else:
            order = [(opponent_creature, player_creature, self.opponent_skill),
                    (player_creature, opponent_creature, self.player_skill)]

        # Execute attacks
        for attacker, defender, skill in order:
            if defender.hp <= 0:
                continue
                
            damage = self.calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def run(self):
        while True:
            if self.phase == "player_choice":
                choices = [Button(skill.display_name) for skill in self.player.creatures[0].skills]
                choice = self._wait_for_choice(self.player, choices)
                self.player_skill = next(s for s in self.player.creatures[0].skills 
                                      if s.display_name == choice.display_name)
                self.phase = "opponent_choice"

            elif self.phase == "opponent_choice":
                choices = [Button(skill.display_name) for skill in self.opponent.creatures[0].skills]
                choice = self._wait_for_choice(self.opponent, choices)
                self.opponent_skill = next(s for s in self.opponent.creatures[0].skills 
                                        if s.display_name == choice.display_name)
                self.phase = "resolution"

            else:  # resolution phase
                self.execute_turn()
                
                # Check win condition
                if self.player.creatures[0].hp <= 0:
                    self._show_text(self.player, "You lost!")
                    break
                elif self.opponent.creatures[0].hp <= 0:
                    self._show_text(self.player, "You won!")
                    break
                    
                self.phase = "player_choice"

        # Reset creature states
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
            
        self._transition_to_scene("MainMenuScene")
