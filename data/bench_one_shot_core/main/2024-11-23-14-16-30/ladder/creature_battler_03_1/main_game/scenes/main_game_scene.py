from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_actions = {}  # Will store {player_uid: skill}

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")

        while True:
            # Player Choice Phase
            self.handle_turn_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.handle_turn_choice(self.opponent, self.opponent_creature)

            # Resolution Phase
            self.resolve_turn()

            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene")  # Return to menu after battle
                return
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")  # Return to menu after battle
                return

    def handle_turn_choice(self, current_player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        selected_skill = next(skill for skill in creature.skills 
                            if skill.display_name == choice.display_name)
        self.queued_actions[current_player.uid] = selected_skill

    def resolve_turn(self):
        # Determine order based on speed
        first_uid = self.player.uid
        second_uid = self.opponent.uid
        if self.opponent_creature.speed > self.player_creature.speed:
            first_uid, second_uid = second_uid, first_uid
        elif self.opponent_creature.speed == self.player_creature.speed:
            if random.random() < 0.5:
                first_uid, second_uid = second_uid, first_uid

        # Execute skills in order
        for attacker_uid in [first_uid, second_uid]:
            attacker = self.player if attacker_uid == self.player.uid else self.opponent
            defender = self.opponent if attacker_uid == self.player.uid else self.player
            attacker_creature = self.player_creature if attacker_uid == self.player.uid else self.opponent_creature
            defender_creature = self.opponent_creature if attacker_uid == self.player.uid else self.player_creature
            
            skill = self.queued_actions[attacker_uid]
            
            # Calculate damage
            raw_damage = (attacker_creature.attack + skill.base_damage - defender_creature.defense)
            
            # Apply type effectiveness
            multiplier = self.get_type_multiplier(skill.skill_type, defender_creature.creature_type)
            final_damage = int(raw_damage * multiplier)
            
            # Apply damage
            defender_creature.hp = max(0, defender_creature.hp - final_damage)
            
            # Show result
            effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
            self._show_text(self.player, 
                f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness} Dealt {final_damage} damage!")
            self._show_text(self.opponent, 
                f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness} Dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
