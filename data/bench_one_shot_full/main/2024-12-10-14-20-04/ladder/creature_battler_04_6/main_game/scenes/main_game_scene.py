from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_choice = None
        self.opponent_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender_creature.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def execute_turn(self):
        # Determine order
        creatures = [(self.player_creature, self.player_choice), (self.opponent_creature, self.opponent_choice)]
        if self.player_creature.speed == self.opponent_creature.speed:
            random.shuffle(creatures)
        else:
            creatures.sort(key=lambda x: x[0].speed, reverse=True)

        # Execute moves
        for attacker, skill in creatures:
            if attacker == self.player_creature:
                defender = self.opponent_creature
                attacker_name = self.player.display_name
            else:
                defender = self.player_creature
                attacker_name = self.opponent.display_name

            damage = self.calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(self.player, f"{attacker_name}'s {attacker.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"It dealt {damage} damage!")

            if defender.hp == 0:
                return True
        return False

    def run(self):
        while True:
            # Player choice phase
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.player_choice = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)

            # Opponent choice phase
            opponent_choice = self._wait_for_choice(self.opponent, [Button(skill.display_name) for skill in self.opponent_creature.skills])
            self.opponent_choice = next(s for s in self.opponent_creature.skills if s.display_name == opponent_choice.display_name)

            # Resolution phase
            battle_ended = self.execute_turn()
            
            if battle_ended:
                if self.player_creature.hp == 0:
                    self._show_text(self.player, "You lost!")
                else:
                    self._show_text(self.player, "You won!")
                    
                # Reset creatures before transitioning
                self.player_creature.hp = self.player_creature.max_hp
                self.opponent_creature.hp = self.opponent_creature.max_hp
                self._transition_to_scene("MainMenuScene")
                return
