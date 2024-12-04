from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")

        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent Choice Phase  
            self.opponent_chosen_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution Phase
            first, second = self.determine_order()
            
            # Execute moves
            if not self.execute_skill(first[0], first[1], first[2], first[3]):
                break
            if not self.execute_skill(second[0], second[1], second[2], second[3]):
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill), \
                   (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill), \
                   (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill), \
                       (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill)
            else:
                return (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill), \
                       (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill)

    def execute_skill(self, attacker, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender_creature.hp -= final_damage
        
        # Show damage message
        message = f"{attacker_creature.display_name} used {skill.display_name} for {final_damage} damage!"
        self._show_text(attacker, message)
        self._show_text(self.opponent if attacker == self.player else self.player, message)
        
        # Check if battle should end
        if defender_creature.hp <= 0:
            defender_creature.hp = 0
            winner = attacker
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._show_text(self.opponent, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return False
            
        return True

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)
