from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
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
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase  
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution Phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute skills in order
            self._execute_skill(*first)
            if not self._check_battle_end():
                self._execute_skill(*second)
                if self._check_battle_end():
                    break
            else:
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _determine_order(self, action1, action2):
        p1, c1, _ = action1
        p2, c2, _ = action2
        
        if c1.speed > c2.speed:
            return action1, action2
        elif c2.speed > c1.speed:
            return action2, action1
        else:
            return (action1, action2) if random.random() < 0.5 else (action2, action1)

    def _calculate_damage(self, attacker, skill, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        factor = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": factor = 2.0
            elif defender.creature_type == "water": factor = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": factor = 2.0
            elif defender.creature_type == "leaf": factor = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": factor = 2.0
            elif defender.creature_type == "fire": factor = 0.5

        return int(raw_damage * factor)

    def _execute_skill(self, player, attacker, skill):
        if player == self.player:
            defender = self.opponent_creature
        else:
            defender = self.player_creature
            
        damage = self._calculate_damage(attacker, skill, defender)
        defender.hp = max(0, defender.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
        self._show_text(self.opponent, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.opponent, "You won!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.opponent, "You lost!")
            return True
        return False
