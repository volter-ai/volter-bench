from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.opponent_chosen_skill = self._handle_player_turn(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolve_turn()
            
            # Check for battle end
            if self._check_battle_end():
                break

    def _handle_player_turn(self, current_player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _resolve_turn(self):
        first, second = self._determine_turn_order()
        
        # Execute first skill
        self._execute_skill(first[0], first[1], first[2], first[3])
        if not self._check_battle_end():
            # Execute second skill if battle hasn't ended
            self._execute_skill(second[0], second[1], second[2], second[3])

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature), \
                   (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature), \
                   (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature), \
                       (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature)
            else:
                return (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature), \
                       (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature)

    def _execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= damage
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")
        self._show_text(self.opponent, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
