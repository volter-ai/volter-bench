from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self._reset_creatures()

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Choose your skill:
{[skill.display_name for skill in self.player_creature.skills]}
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
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }

        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _execute_turn(self, first, second, first_skill, second_skill):
        # Execute first attack
        damage = self._calculate_damage(first, second, first_skill)
        second.hp -= damage
        self._show_text(self.player, f"{first.display_name} used {first_skill.display_name} for {damage} damage!")
        
        # If second creature still alive, execute second attack
        if second.hp > 0:
            damage = self._calculate_damage(second, first, second_skill)
            first.hp -= damage
            self._show_text(self.player, f"{second.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Bot choice phase
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

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
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene") 
                break
