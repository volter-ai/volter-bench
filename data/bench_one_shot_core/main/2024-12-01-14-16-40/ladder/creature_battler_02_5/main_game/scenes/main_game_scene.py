from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._handle_player_turn()
            
            # Opponent Choice Phase
            opponent_skill = self._handle_opponent_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self.player_creature.hp == 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene")
            elif self.opponent_creature.hp == 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _handle_opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order based on speed
        first = (self.player, self.player_creature, player_skill)
        second = (self.opponent, self.opponent_creature, opponent_skill)
        
        if second[1].speed > first[1].speed or (second[1].speed == first[1].speed and random.random() > 0.5):
            first, second = second, first

        for attacker, attacker_creature, skill in [first, second]:
            if attacker == self.player:
                defender_creature = self.opponent_creature
            else:
                defender_creature = self.player_creature

            damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
            defender_creature.hp = max(0, defender_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
            self._show_text(attacker, f"Dealt {damage} damage!")

            if defender_creature.hp == 0:
                break
