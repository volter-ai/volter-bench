from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self.player_creature.hp == 0:
                self._show_text(self.player, "You lost the battle!")
                self._quit_whole_game()  # End game on loss
            elif self.opponent_creature.hp == 0:
                self._show_text(self.player, "You won the battle!")
                self._transition_to_scene("MainMenuScene")  # Return to menu on win

    def _get_skill_choice(self, actor, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(actor, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order based on speed
        first = (self.player, self.player_creature, player_skill)
        second = (self.opponent, self.opponent_creature, opponent_skill)
        
        if self.opponent_creature.speed > self.player_creature.speed or \
           (self.opponent_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first, second = second, first

        for attacker, attacker_creature, skill in [first, second]:
            if attacker == self.player:
                defender_creature = self.opponent_creature
            else:
                defender_creature = self.player_creature

            damage = skill.base_damage + attacker_creature.attack - defender_creature.defense
            damage = max(0, damage)  # Prevent negative damage
            defender_creature.hp = max(0, defender_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
            self._show_text(attacker, f"Dealt {damage} damage!")
            
            if defender_creature.hp == 0:
                break
