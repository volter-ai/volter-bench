from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent choice phase
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._cleanup_and_exit()
                return
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._cleanup_and_exit()
                return

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order
        first_attacker, first_skill, first_target = self._determine_first(
            (self.player, player_skill, self.opponent_creature),
            (self.opponent, opponent_skill, self.player_creature)
        )
        second_attacker, second_skill, second_target = self._determine_second(
            (self.player, player_skill, self.opponent_creature),
            (self.opponent, opponent_skill, self.player_creature)
        )

        # Execute skills
        self._execute_skill(first_attacker, first_skill, first_target)
        if second_target.hp > 0:  # Only execute second skill if target still alive
            self._execute_skill(second_attacker, second_skill, second_target)

    def _determine_first(self, pair1, pair2):
        attacker1, skill1, target1 = pair1
        attacker2, skill2, target2 = pair2
        
        if attacker1.creatures[0].speed > attacker2.creatures[0].speed:
            return pair1
        elif attacker2.creatures[0].speed > attacker1.creatures[0].speed:
            return pair2
        else:
            return random.choice([pair1, pair2])

    def _determine_second(self, pair1, pair2):
        first = self._determine_first(pair1, pair2)
        return pair2 if first == pair1 else pair1

    def _execute_skill(self, attacker, skill, target):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.creatures[0].attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.creatures[0].sp_attack / target.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        target.hp = max(0, target.hp - final_damage)
        
        # Show result
        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")

    def _get_type_multiplier(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def _cleanup_and_exit(self):
        # Reset creature states by setting hp back to max_hp
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")
