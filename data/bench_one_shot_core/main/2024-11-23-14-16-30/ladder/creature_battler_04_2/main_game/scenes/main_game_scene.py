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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent choice phase
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check win condition
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

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
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

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order
        first, second = self._determine_order(
            (self.player, self.player_creature, player_skill),
            (self.opponent, self.opponent_creature, opponent_skill)
        )

        # Execute turns
        for attacker, creature, skill in [first, second]:
            if attacker == self.player:
                defender = self.opponent_creature
            else:
                defender = self.player_creature

            damage = self._calculate_damage(creature, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(self.player, f"{creature.display_name} used {skill.display_name} for {damage} damage!")
            
            if defender.hp <= 0:
                break

    def _determine_order(self, player_data, opponent_data):
        player_creature = player_data[1]
        opponent_creature = opponent_data[1]
        
        if player_creature.speed > opponent_creature.speed:
            return player_data, opponent_data
        elif player_creature.speed < opponent_creature.speed:
            return opponent_data, player_data
        else:
            return random.choice([(player_data, opponent_data), (opponent_data, player_data)])

    def _cleanup_and_exit(self):
        # Reset creatures by setting HP back to max
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")
