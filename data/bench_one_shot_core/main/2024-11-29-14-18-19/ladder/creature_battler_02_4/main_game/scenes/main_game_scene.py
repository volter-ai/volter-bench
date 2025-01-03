from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            self.player_choice = self._wait_for_choice(self.player, 
                [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills])

            # Opponent Choice Phase
            self.opponent_choice = self._wait_for_choice(self.opponent,
                [DictionaryChoice(skill.display_name) for skill in self.opponent_creature.skills])

            # Resolution Phase
            if self.player_creature.speed > self.opponent_creature.speed:
                self.resolve_turn(self.player_creature, self.opponent_creature)
                if self.check_battle_end(): break
                self.resolve_turn(self.opponent_creature, self.player_creature)
            elif self.player_creature.speed < self.opponent_creature.speed:
                self.resolve_turn(self.opponent_creature, self.player_creature)
                if self.check_battle_end(): break
                self.resolve_turn(self.player_creature, self.opponent_creature)
            else:
                if random.random() < 0.5:
                    self.resolve_turn(self.player_creature, self.opponent_creature)
                    if self.check_battle_end(): break
                    self.resolve_turn(self.opponent_creature, self.player_creature)
                else:
                    self.resolve_turn(self.opponent_creature, self.player_creature)
                    if self.check_battle_end(): break
                    self.resolve_turn(self.player_creature, self.opponent_creature)
            
            if self.check_battle_end():
                break

    def resolve_turn(self, attacker, defender):
        skill = attacker.skills[0]  # For now just use tackle
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp -= damage
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
