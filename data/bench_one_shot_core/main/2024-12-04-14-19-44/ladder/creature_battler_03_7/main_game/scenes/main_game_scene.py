from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
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
        
        status = f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

Phase: {self.phase}
"""
        if self.phase == "player_choice":
            status += "\nChoose your skill:"
            for skill in player_creature.skills:
                status += f"\n> {skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)"
                
        return status

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                multiplier = 2.0
            elif defender_creature.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                multiplier = 2.0
            elif defender_creature.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                multiplier = 2.0
            elif defender_creature.creature_type == "fire":
                multiplier = 0.5
                
        return int(raw_damage * multiplier)

    def execute_turn(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        
        first = player_creature if player_creature.speed > opponent_creature.speed else opponent_creature
        second = opponent_creature if first == player_creature else player_creature
        first_skill = self.player_skill if first == player_creature else self.opponent_skill
        second_skill = self.opponent_skill if first == player_creature else self.player_skill
        
        if player_creature.speed == opponent_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                first_skill, second_skill = second_skill, first_skill

        # First attack
        damage = self.calculate_damage(first, second, first_skill)
        second.hp -= damage
        self._show_text(self.player, f"{first.display_name} used {first_skill.display_name} for {damage} damage!")
        
        if second.hp <= 0:
            return first == player_creature
            
        # Second attack
        damage = self.calculate_damage(second, first, second_skill)
        first.hp -= damage
        self._show_text(self.player, f"{second.display_name} used {second_skill.display_name} for {damage} damage!")
        
        if first.hp <= 0:
            return first != player_creature
            
        return None

    def run(self):
        while True:
            if self.phase == "player_choice":
                choices = [SelectThing(skill) for skill in self.player.creatures[0].skills]
                self.player_skill = self._wait_for_choice(self.player, choices).thing
                self.phase = "opponent_choice"
                
            elif self.phase == "opponent_choice":
                choices = [SelectThing(skill) for skill in self.opponent.creatures[0].skills]
                self.opponent_skill = self._wait_for_choice(self.opponent, choices).thing
                self.phase = "resolution"
                
            else: # resolution phase
                result = self.execute_turn()
                if result is not None:
                    if result:
                        self._show_text(self.player, "You won!")
                    else:
                        self._show_text(self.player, "You lost!")
                    self._transition_to_scene("MainMenuScene")
                    return
                    
                self.phase = "player_choice"
