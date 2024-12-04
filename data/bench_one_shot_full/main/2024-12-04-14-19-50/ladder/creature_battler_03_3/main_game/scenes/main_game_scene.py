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
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player phase
            player_skill = self._handle_player_turn()
            
            # Opponent phase  
            opponent_skill = self._handle_opponent_turn()

            # Resolution phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self._check_battle_end():
                # Present post-battle choices
                menu_button = Button("Return to Main Menu")
                quit_button = Button("Quit Game")
                choice = self._wait_for_choice(self.player, [menu_button, quit_button])
                
                if choice == menu_button:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
                return

    def _handle_player_turn(self):
        self._show_text(self.player, "Choose your skill!")
        skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, skill_choices)
        # Map the button choice back to the actual skill object
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _handle_opponent_turn(self):
        skill_choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, skill_choices)
        # Map the button choice back to the actual skill object
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5
            
        return int(raw_damage * multiplier)

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order based on speed, with random resolution for ties
        if self.player_creature.speed == self.opponent_creature.speed:
            # Random order when speeds are equal
            creatures = [self.player_creature, self.opponent_creature]
            first = random.choice(creatures)
            second = self.opponent_creature if first == self.player_creature else self.player_creature
        else:
            # Higher speed goes first
            first = self.player_creature if self.player_creature.speed > self.opponent_creature.speed else self.opponent_creature
            second = self.opponent_creature if first == self.player_creature else self.player_creature
        
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        # Execute skills
        if first == self.player_creature:
            damage = self._calculate_damage(self.player_creature, self.opponent_creature, first_skill)
            self.opponent_creature.hp -= damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {first_skill.display_name} for {damage} damage!")
            
            if self.opponent_creature.hp > 0:
                damage = self._calculate_damage(self.opponent_creature, self.player_creature, second_skill)
                self.player_creature.hp -= damage
                self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {second_skill.display_name} for {damage} damage!")
        else:
            damage = self._calculate_damage(self.opponent_creature, self.player_creature, first_skill)
            self.player_creature.hp -= damage
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {first_skill.display_name} for {damage} damage!")
            
            if self.player_creature.hp > 0:
                damage = self._calculate_damage(self.player_creature, self.opponent_creature, second_skill)
                self.opponent_creature.hp -= damage
                self._show_text(self.player, f"Your {self.player_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
