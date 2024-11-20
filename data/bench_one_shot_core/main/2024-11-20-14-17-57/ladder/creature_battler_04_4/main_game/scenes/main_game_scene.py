from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.phase = "player_choice"
        self.player_skill = None
        self.opponent_skill = None
        
        # Reset creatures to full HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Opponent's {opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

Phase: {self.phase}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                effectiveness = 2.0
            elif defender_creature.creature_type == "water":
                effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                effectiveness = 2.0
            elif defender_creature.creature_type == "leaf":
                effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                effectiveness = 2.0
            elif defender_creature.creature_type == "fire":
                effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def run(self):
        while True:
            # Player choice phase
            self.phase = "player_choice"
            player_creature = self.player.creatures[0]
            choices = [Button(skill.display_name) for skill in player_creature.skills]
            choice = self._wait_for_choice(self.player, choices)
            self.player_skill = player_creature.skills[choices.index(choice)]

            # Opponent choice phase  
            self.phase = "opponent_choice"
            opponent_creature = self.opponent.creatures[0]
            choices = [Button(skill.display_name) for skill in opponent_creature.skills]
            choice = self._wait_for_choice(self.opponent, choices)
            self.opponent_skill = opponent_creature.skills[choices.index(choice)]

            # Resolution phase
            self.phase = "resolution"
            
            # Determine order
            if player_creature.speed > opponent_creature.speed:
                first = (self.player, player_creature, self.player_skill)
                second = (self.opponent, opponent_creature, self.opponent_skill)
            elif opponent_creature.speed > player_creature.speed:
                first = (self.opponent, opponent_creature, self.opponent_skill)
                second = (self.player, player_creature, self.player_skill)
            else:
                if random.random() < 0.5:
                    first = (self.player, player_creature, self.player_skill)
                    second = (self.opponent, opponent_creature, self.opponent_skill)
                else:
                    first = (self.opponent, opponent_creature, self.opponent_skill)
                    second = (self.player, player_creature, self.player_skill)

            # Execute moves
            for attacker, attacker_creature, skill in [first, second]:
                if attacker == self.player:
                    defender = self.opponent
                    defender_creature = opponent_creature
                else:
                    defender = self.player
                    defender_creature = player_creature

                damage = self.calculate_damage(attacker_creature, defender_creature, skill)
                defender_creature.hp -= damage
                
                self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"It dealt {damage} damage!")

                if defender_creature.hp <= 0:
                    defender_creature.hp = 0
                    if defender == self.player:
                        self._show_text(self.player, "You lost!")
                    else:
                        self._show_text(self.player, "You won!")
                    self._transition_to_scene("MainMenuScene")
                    return
