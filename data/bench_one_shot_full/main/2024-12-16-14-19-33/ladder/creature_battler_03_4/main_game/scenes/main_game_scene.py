from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")

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

            # Execute moves in order
            for attacker, creature, skill in [first, second]:
                if self._execute_skill(attacker, creature, skill):
                    return  # Battle ended

    def _get_skill_choice(self, player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        for choice, skill in zip(choices, creature.skills):
            choice.value = {"skill": skill}
        
        return self._wait_for_choice(player, choices).value["skill"]

    def _determine_order(self, first_pair, second_pair):
        if first_pair[1].speed > second_pair[1].speed:
            return first_pair, second_pair
        elif first_pair[1].speed < second_pair[1].speed:
            return second_pair, first_pair
        else:
            return random.sample([first_pair, second_pair], 2)

    def _execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.opponent
            defender_creature = self.opponent_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        # Calculate damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Apply type effectiveness
        factor = self._get_type_effectiveness(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * factor)
        
        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        # Show result
        message = f"{attacker_creature.display_name} used {skill.display_name}! "
        if factor > 1:
            message += "It's super effective! "
        elif factor < 1:
            message += "It's not very effective... "
        message += f"Dealt {final_damage} damage!"
        
        self._show_text(self.player, message)
        self._show_text(self.opponent, message)

        # Check for battle end
        if defender_creature.hp <= 0:
            winner = attacker.display_name
            self._show_text(self.player, f"{winner} wins!")
            self._show_text(self.opponent, f"{winner} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        
        return False

    def _get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
