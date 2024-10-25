from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
            battle_result = self.battle_loop()
            
            if battle_result == "quit":
                self._quit_whole_game()
                return
            
            play_again = self.ask_play_again()
            if not play_again:
                self._transition_to_scene("MainMenuScene")
                return
            
            # Reset creatures for the next battle
            self.player_creature.hp = self.player_creature.max_hp
            self.opponent_creature.hp = self.opponent_creature.max_hp

    def battle_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            if player_skill == "quit":
                return "quit"

            # Foe Choice Phase
            opponent_skill = self.foe_choice_phase()

            # Resolution Phase
            self.resolution_phase(player_skill, opponent_skill)

            # Check for battle end
            if self.check_battle_end():
                return "battle_end"

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        quit_button = Button("Quit")
        choices.append(quit_button)
        
        choice = self._wait_for_choice(self.player, choices)
        
        if choice == quit_button:
            return "quit"
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
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
            # If speeds are equal, randomly choose who goes first
            first_attacker, first_creature, first_skill, second_attacker, second_creature, second_skill = random.choice([
                (self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature, opponent_skill),
                (self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature, player_skill)
            ])
            
            self.execute_skill(first_attacker, first_creature, first_skill, second_creature)
            if second_creature.hp > 0:
                self.execute_skill(second_attacker, second_creature, second_skill, first_creature)

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False

    def ask_play_again(self):
        play_again_button = Button("Play Again")
        main_menu_button = Button("Main Menu")
        choices = [play_again_button, main_menu_button]
        
        self._show_text(self.player, "Do you want to play again?")
        choice = self._wait_for_choice(self.player, choices)
        
        return choice == play_again_button
