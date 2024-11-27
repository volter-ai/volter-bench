from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self._reset_creatures()

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        # Return final damage as integer
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _get_creature_owner(self, creature):
        if creature == self.player_creature:
            return self.player
        return self.opponent

    def _execute_turn(self, first_creature, second_creature, first_skill, second_skill):
        # Get the owners (players) for each creature
        first_player = self._get_creature_owner(first_creature)
        second_player = self._get_creature_owner(second_creature)

        # First attack
        damage = self._calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(first_player, f"{first_creature.display_name} used {first_skill.display_name}!")
        self._show_text(first_player, f"It dealt {damage} damage!")
        self._show_text(second_player, f"{first_creature.display_name} used {first_skill.display_name}!")
        self._show_text(second_player, f"It dealt {damage} damage!")

        # Check if battle ended
        if second_creature.hp <= 0:
            return

        # Second attack
        damage = self._calculate_damage(second_creature, first_creature, second_skill)
        first_creature.hp -= damage
        self._show_text(second_player, f"{second_creature.display_name} used {second_skill.display_name}!")
        self._show_text(second_player, f"It dealt {damage} damage!")
        self._show_text(first_player, f"{second_creature.display_name} used {second_skill.display_name}!")
        self._show_text(first_player, f"It dealt {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Determine turn order
            if self.player_creature.speed > self.opponent_creature.speed:
                first, second = self.player_creature, self.opponent_creature
                first_skill, second_skill = player_skill, opponent_skill
            elif self.player_creature.speed < self.opponent_creature.speed:
                first, second = self.opponent_creature, self.player_creature
                first_skill, second_skill = opponent_skill, player_skill
            else:
                if random.random() < 0.5:
                    first, second = self.player_creature, self.opponent_creature
                    first_skill, second_skill = player_skill, opponent_skill
                else:
                    first, second = self.opponent_creature, self.player_creature
                    first_skill, second_skill = opponent_skill, player_skill

            # Execute turn
            self._execute_turn(first, second, first_skill, second_skill)

            # Check win conditions
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.opponent, "You lost!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._show_text(self.opponent, "You won!")
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")
