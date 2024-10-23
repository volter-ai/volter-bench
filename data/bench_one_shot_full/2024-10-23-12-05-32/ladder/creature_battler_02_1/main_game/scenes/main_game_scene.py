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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player)
            
            # Foe Choice Phase
            opponent_skill = self._foe_choice_phase(self.opponent)
            
            # Resolution Phase
            self._resolution_phase(player_skill, opponent_skill)
            
            # Check for battle end
            battle_end, player_won = self._check_battle_end()
            if battle_end:
                if player_won:
                    self._show_text(self.player, "You won the battle!")
                else:
                    self._show_text(self.player, "You lost the battle!")
                
                # Ask if the player wants to play again or quit
                play_again_button = Button("Play Again")
                quit_button = Button("Quit")
                choice = self._wait_for_choice(self.player, [play_again_button, quit_button])
                
                if choice == play_again_button:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
                break

    def _player_choice_phase(self, player):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _foe_choice_phase(self, opponent):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(opponent, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, opponent_skill):
        first, second = self._determine_order(self.player_creature, self.opponent_creature, player_skill, opponent_skill)
        
        self._execute_skill(first[0], first[1], second[1], first[2])
        if self._check_battle_end()[0]:
            return
        
        self._execute_skill(second[0], second[1], first[1], second[2])

    def _determine_order(self, creature1, creature2, skill1, skill2):
        if creature1.speed > creature2.speed:
            return (self.player, self.player_creature, skill1), (self.opponent, self.opponent_creature, skill2)
        elif creature2.speed > creature1.speed:
            return (self.opponent, self.opponent_creature, skill2), (self.player, self.player_creature, skill1)
        else:
            if random.choice([True, False]):
                return (self.player, self.player_creature, skill1), (self.opponent, self.opponent_creature, skill2)
            else:
                return (self.opponent, self.opponent_creature, skill2), (self.player, self.player_creature, skill1)

    def _execute_skill(self, attacker, attacker_creature, defender_creature, skill):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            return True, False  # Battle ended, player lost
        elif self.opponent_creature.hp <= 0:
            return True, True  # Battle ended, player won
        return False, False  # Battle not ended
