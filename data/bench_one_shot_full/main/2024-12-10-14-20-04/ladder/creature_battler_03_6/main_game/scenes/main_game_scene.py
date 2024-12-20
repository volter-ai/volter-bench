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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._handle_player_turn()
            
            # Opponent Choice Phase  
            opponent_skill = self._handle_opponent_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self._check_battle_end():
                # Instead of breaking, transition back to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def _handle_player_turn(self):
        self._show_text(self.player, "Choose your skill!")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        return self._wait_for_choice(self.player, choices).thing

    def _handle_opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        return self._wait_for_choice(self.opponent, choices).thing

    def _calculate_damage(self, skill, attacker, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5
            
        return int(raw_damage * multiplier)

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player, self.player_creature, player_skill)
            second = (self.opponent, self.opponent_creature, opponent_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            first = (self.opponent, self.opponent_creature, opponent_skill)
            second = (self.player, self.player_creature, player_skill)
        else:
            if random.random() < 0.5:
                first = (self.player, self.player_creature, player_skill)
                second = (self.opponent, self.opponent_creature, opponent_skill)
            else:
                first = (self.opponent, self.opponent_creature, opponent_skill)
                second = (self.player, self.player_creature, player_skill)

        # Execute moves in order
        for attacker, attacker_creature, skill in [first, second]:
            if attacker == self.player:
                defender = self.opponent
                defender_creature = self.opponent_creature
            else:
                defender = self.player
                defender_creature = self.player_creature

            damage = self._calculate_damage(skill, attacker_creature, defender_creature)
            defender_creature.hp = max(0, defender_creature.hp - damage)
            
            self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"It dealt {damage} damage!")
            
            if defender_creature.hp == 0:
                break

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
            return True
        return False
