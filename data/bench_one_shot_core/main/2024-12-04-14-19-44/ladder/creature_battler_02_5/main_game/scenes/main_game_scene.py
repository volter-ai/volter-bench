from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.opponent_chosen_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolve_turn()
            
            # Check for battle end
            if self._check_battle_end():
                # Ask player if they want to play again
                play_again_button = Button("Play Again")
                quit_button = Button("Quit")
                
                choice = self._wait_for_choice(self.player, [play_again_button, quit_button])
                
                if choice == play_again_button:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
                return

    def _get_skill_choice(self, acting_player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(acting_player, choices).thing

    def _resolve_turn(self):
        first, second = self._determine_turn_order()
        
        self._execute_skill(first[0], first[1], first[2], second[2])
        if second[2].hp > 0:  # Only execute second skill if target still alive
            self._execute_skill(second[0], second[1], second[2], first[2])

    def _determine_turn_order(self):
        player_speed = self.player_creature.speed
        opponent_speed = self.opponent_creature.speed
        
        if player_speed > opponent_speed:
            first = (self.player, self.player_chosen_skill, self.player_creature)
            second = (self.opponent, self.opponent_chosen_skill, self.opponent_creature)
        elif opponent_speed > player_speed:
            first = (self.opponent, self.opponent_chosen_skill, self.opponent_creature)
            second = (self.player, self.player_chosen_skill, self.player_creature)
        else:
            if random.random() < 0.5:
                first = (self.player, self.player_chosen_skill, self.player_creature)
                second = (self.opponent, self.opponent_chosen_skill, self.opponent_creature)
            else:
                first = (self.opponent, self.opponent_chosen_skill, self.opponent_creature)
                second = (self.player, self.player_chosen_skill, self.player_creature)
        return first, second

    def _execute_skill(self, attacker, skill, attacker_creature, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(0, damage)  # Prevent negative damage
        defender_creature.hp -= damage
        defender_creature.hp = max(0, defender_creature.hp)  # Prevent negative HP
        
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
