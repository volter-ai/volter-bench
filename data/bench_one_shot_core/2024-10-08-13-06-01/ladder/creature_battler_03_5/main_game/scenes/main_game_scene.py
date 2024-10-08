from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.turn_count = 0

    def __str__(self):
        return f"""===Battle===
Turn: {self.turn_count}

{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}

{self.opponent.display_name}'s {self.opponent_creature.display_name}
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

> Use Skill
> Quit
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            self.turn_count += 1
            
            # Player turn
            player_skill = self.player_choose_skill()
            
            # Opponent turn
            opponent_skill = self.opponent_choose_skill()
            
            # Resolve turn
            self.resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self.check_battle_end():
                self.handle_battle_end()
                break

    def player_choose_skill(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choice = self._wait_for_choice(self.player, [use_skill_button, quit_button])
        
        if choice == quit_button:
            self._quit_whole_game()
        
        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        return self._wait_for_choice(self.player, skill_choices).thing

    def opponent_choose_skill(self):
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        return self._wait_for_choice(self.opponent, skill_choices).thing

    def resolve_turn(self, player_skill, opponent_skill):
        first, second = self.determine_turn_order(player_skill, opponent_skill)
        self.execute_skill(*first)
        if not self.check_battle_end():
            self.execute_skill(*second)

    def determine_turn_order(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, player_skill, self.opponent_creature), (self.opponent, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, opponent_skill, self.player_creature), (self.player, player_skill, self.opponent_creature)
        else:
            if random.choice([True, False]):
                return (self.player, player_skill, self.opponent_creature), (self.opponent, opponent_skill, self.player_creature)
            else:
                return (self.opponent, opponent_skill, self.player_creature), (self.player, player_skill, self.opponent_creature)

    def execute_skill(self, attacker, skill, target):
        raw_damage = attacker.creatures[0].attack + skill.base_damage - target.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, target.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        target.hp = max(0, target.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {target.display_name}!")

    def calculate_weakness_factor(self, skill_type, target_type):
        if skill_type == "normal":
            return 1
        elif skill_type == "fire" and target_type == "leaf":
            return 2
        elif skill_type == "fire" and target_type == "water":
            return 0.5
        elif skill_type == "water" and target_type == "fire":
            return 2
        elif skill_type == "water" and target_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and target_type == "water":
            return 2
        elif skill_type == "leaf" and target_type == "fire":
            return 0.5
        else:
            return 1

    def check_battle_end(self):
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def handle_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")

        main_menu_button = Button("Return to Main Menu")
        quit_button = Button("Quit Game")
        choice = self._wait_for_choice(self.player, [main_menu_button, quit_button])

        if choice == main_menu_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
