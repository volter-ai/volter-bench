from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}

Opponent's skills:
{self._format_skills(self.opponent_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)" for skill in skills])

    def run(self):
        while True:
            battle_result = self.game_loop()
            if battle_result == "quit":
                self._quit_whole_game()
                return
            
            play_again = Button("Play Again")
            quit_game = Button("Quit Game")
            choice = self._wait_for_choice(self.player, [play_again, quit_game])
            
            if choice == quit_game:
                self._quit_whole_game()
                return
            elif choice == play_again:
                # Reset creatures for a new battle
                self.player_creature.hp = self.player_creature.max_hp
                self.opponent_creature.hp = self.opponent_creature.max_hp
            else:
                self._transition_to_scene("MainMenuScene")
                return

    def game_loop(self):
        while True:
            self._show_text(self.player, str(self))
            
            player_skill = self.player_choice_phase()
            if player_skill == "quit":
                return "quit"
            
            opponent_skill = self.foe_choice_phase()
            
            self.resolution_phase(player_skill, opponent_skill)
            
            if self.check_battle_end():
                return "battle_end"

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        quit_button = Button("Quit Game")
        choices.append(quit_button)
        
        choice = self._wait_for_choice(self.player, choices)
        
        if choice == quit_button:
            return "quit"
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            # Equal speed, randomly decide who goes first
            if random.choice([True, False]):
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
                if self.opponent_creature.hp > 0:
                    self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            else:
                self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
                if self.player_creature.hp > 0:
                    self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender_creature.display_name}!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5},
            "normal": {}  # Normal type is neither effective nor ineffective against any type
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}, you have lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"Congratulations {self.player.display_name}, you have won the battle!")
            return True
        return False
