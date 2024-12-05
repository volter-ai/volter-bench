from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} - {skill.base_damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._handle_player_turn()
            
            # Opponent Choice Phase  
            opponent_skill = self._handle_opponent_turn()

            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)

            # Check for battle end
            if self._check_battle_end():
                break

    def _handle_player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _handle_opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
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

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order
        first = self.player_creature if self.player_creature.speed > self.opponent_creature.speed else self.opponent_creature
        second = self.opponent_creature if first == self.player_creature else self.player_creature
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        # If speeds are equal, randomize
        if self.player_creature.speed == self.opponent_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                first_skill, second_skill = second_skill, first_skill

        # Execute first attack
        if first == self.player_creature:
            damage = self._calculate_damage(self.player_creature, self.opponent_creature, first_skill)
            self.opponent_creature.hp -= damage
            self._show_text(self.player, f"{self.player_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        else:
            damage = self._calculate_damage(self.opponent_creature, self.player_creature, first_skill)
            self.player_creature.hp -= damage
            self._show_text(self.player, f"{self.opponent_creature.display_name} used {first_skill.display_name} for {damage} damage!")

        # Check if battle should continue
        if not self._check_battle_end():
            # Execute second attack
            if second == self.player_creature:
                damage = self._calculate_damage(self.player_creature, self.opponent_creature, second_skill)
                self.opponent_creature.hp -= damage
                self._show_text(self.player, f"{self.player_creature.display_name} used {second_skill.display_name} for {damage} damage!")
            else:
                damage = self._calculate_damage(self.opponent_creature, self.player_creature, second_skill)
                self.player_creature.hp -= damage
                self._show_text(self.player, f"{self.opponent_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} was defeated! You lose!")
            self._quit_whole_game()
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} was defeated! You win!")
            self._quit_whole_game()
            return True
        return False
