from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player.display_name} vs {self.opponent.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.opponent_chosen_skill = self._handle_player_turn(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolve_turn()
            
            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, current_player, current_creature):
        choices = [Button(skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return next(skill for skill in current_creature.skills if skill.display_name == choice.display_name)

    def _calculate_damage(self, attacker, skill, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        final_damage = int(raw_damage * effectiveness)
        return max(1, final_damage)  # Minimum 1 damage

    def _get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _resolve_turn(self):
        # Determine order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player, self.player_creature, self.player_chosen_skill)
            second = (self.opponent, self.opponent_creature, self.opponent_chosen_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            first = (self.opponent, self.opponent_creature, self.opponent_chosen_skill)
            second = (self.player, self.player_creature, self.player_chosen_skill)
        else:
            # Random if speed is equal
            if random.random() < 0.5:
                first = (self.player, self.player_creature, self.player_chosen_skill)
                second = (self.opponent, self.opponent_creature, self.opponent_chosen_skill)
            else:
                first = (self.opponent, self.opponent_creature, self.opponent_chosen_skill)
                second = (self.player, self.player_creature, self.player_chosen_skill)

        # Execute moves in order
        for attacker, attacker_creature, skill in [first, second]:
            if attacker == self.player:
                defender = self.opponent
                defender_creature = self.opponent_creature
            else:
                defender = self.player
                defender_creature = self.player_creature

            damage = self._calculate_damage(attacker_creature, skill, defender_creature)
            defender_creature.hp -= damage
            
            self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"It dealt {damage} damage!")
            
            if defender_creature.hp <= 0:
                break
