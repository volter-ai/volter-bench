from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

VS

{self.opponent.display_name}'s {self.opponent_creature.display_name}
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
Attack: {self.opponent_creature.attack}
Defense: {self.opponent_creature.defense}
Speed: {self.opponent_creature.speed}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.opponent_chosen_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            first, second = self._determine_turn_order()
            
            # Execute skills
            self._execute_turn(first)
            if self._check_battle_end():
                break
                
            self._execute_turn(second)
            if self._check_battle_end():
                break

    def _get_skill_choice(self, actor, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(actor, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.sample([self.player, self.opponent], 2)

    def _execute_turn(self, actor):
        attacker = self.player_creature if actor == self.player else self.opponent_creature
        defender = self.opponent_creature if actor == self.player else self.player_creature
        skill = self.player_chosen_skill if actor == self.player else self.opponent_chosen_skill
        
        damage = attacker.attack + skill.base_damage - defender.defense
        damage = max(0, damage)  # Prevent negative damage
        
        defender.hp -= damage
        defender.hp = max(0, defender.hp)  # Prevent negative HP
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
