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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.opponent_chosen_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            first, second = self._determine_turn_order()
            self._resolve_turn(first)
            
            if self._check_battle_end():
                break
                
            self._resolve_turn(second)
            
            if self._check_battle_end():
                break

    def _get_skill_choice(self, actor, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(actor, choices).thing

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_chosen_skill), (self.opponent, self.opponent_chosen_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            return (self.opponent, self.opponent_chosen_skill), (self.player, self.player_chosen_skill)
        else:
            actors = [(self.player, self.player_chosen_skill), (self.opponent, self.opponent_chosen_skill)]
            random.shuffle(actors)
            return actors[0], actors[1]

    def _resolve_turn(self, turn):
        actor, skill = turn
        attacker = self.player_creature if actor == self.player else self.opponent_creature
        defender = self.opponent_creature if actor == self.player else self.player_creature
        
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp = max(0, defender.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
