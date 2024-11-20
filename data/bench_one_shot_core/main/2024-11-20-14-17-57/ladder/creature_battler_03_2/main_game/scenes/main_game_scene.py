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
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, skill_choices)
            self.player_chosen_skill = self.player_creature.skills[skill_choices.index(choice)]

            # Opponent choice phase
            self._show_text(self.opponent, "Opponent choosing skill...")
            opponent_choice = self._wait_for_choice(self.opponent, 
                [Button(skill.display_name) for skill in self.opponent_creature.skills])
            self.opponent_chosen_skill = self.opponent_creature.skills[0]  # Bot will always choose first skill

            # Resolution phase
            first, second = self.determine_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                break
                
            self.execute_turn(second)
            
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.choice([(self.player, self.opponent), (self.opponent, self.player)])

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def execute_turn(self, attacker):
        if attacker == self.player:
            skill = self.player_chosen_skill
            atk_creature = self.player_creature
            def_creature = self.opponent_creature
        else:
            skill = self.opponent_chosen_skill
            atk_creature = self.opponent_creature
            def_creature = self.player_creature

        raw_damage = skill.base_damage + atk_creature.attack - def_creature.defense
        multiplier = self.get_type_multiplier(skill.skill_type, def_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        final_damage = max(1, final_damage)  # Minimum 1 damage

        def_creature.hp = max(0, def_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{atk_creature.display_name} used {skill.display_name}! Dealt {final_damage} damage!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
