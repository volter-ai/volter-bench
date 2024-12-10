from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            player_skill = self.get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            opponent_skill = self.get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution Phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute skills
            self.execute_turn(*first)
            if not self.check_battle_end():
                self.execute_turn(*second)
                if self.check_battle_end():
                    break
            else:
                break

        self._transition_to_scene("MainMenuScene")

    def get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def determine_order(self, player_tuple, opponent_tuple):
        if player_tuple[1].speed > opponent_tuple[1].speed:
            return player_tuple, opponent_tuple
        elif player_tuple[1].speed < opponent_tuple[1].speed:
            return opponent_tuple, player_tuple
        else:
            return random.sample([player_tuple, opponent_tuple], 2)

    def execute_turn(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.opponent
            defender_creature = self.opponent_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        # Calculate damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender_creature.creature_type)
        
        final_damage = int(raw_damage * factor)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender_creature.display_name}")

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} was defeated! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} was defeated! You win!")
            return True
        return False
