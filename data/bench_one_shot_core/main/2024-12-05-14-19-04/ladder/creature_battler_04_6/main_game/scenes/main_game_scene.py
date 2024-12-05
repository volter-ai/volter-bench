from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

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
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute skills
            self._execute_skill(*first)
            if self._check_battle_end():
                break

            if self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
                self._execute_skill(*second)
                if self._check_battle_end():
                    break

        # Reset creature states before transitioning
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        
        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_order(self, action1, action2):
        p1, c1, _ = action1
        p2, c2, _ = action2
        if c1.speed > c2.speed:
            return action1, action2
        elif c2.speed > c1.speed:
            return action2, action1
        else:
            return random.choice([(action1, action2), (action2, action1)])

    def _execute_skill(self, attacker, attacker_creature, skill):
        defender = self.opponent if attacker == self.player else self.player
        defender_creature = self.opponent_creature if attacker == self.player else self.player_creature

        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * multiplier)

        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        # Show result
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"It dealt {final_damage} damage!")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {
                "leaf": 2.0,  # Fire is effective against Leaf
                "water": 0.5  # Fire is ineffective against Water
            },
            "water": {
                "fire": 2.0,  # Water is effective against Fire
                "leaf": 0.5   # Water is ineffective against Leaf
            },
            "leaf": {
                "water": 2.0,  # Leaf is effective against Water
                "fire": 0.5   # Leaf is ineffective against Fire
            }
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
