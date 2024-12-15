from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_skills = {}

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")

        while True:
            # Player Choice Phase
            self.player_choice_phase()
            
            # Opponent Choice Phase  
            self.opponent_choice_phase()
            
            # Resolution Phase
            self.resolution_phase()
            
            # Check for battle end
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.queued_skills[self.player.uid] = choice.thing

    def opponent_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.queued_skills[self.opponent.uid] = choice.thing

    def resolution_phase(self):
        first, second = self.determine_order()
        
        self.execute_skill(first, second)
        if self.check_battle_end():
            return
            
        self.execute_skill(second, first)
        
    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.opponent
        elif self.opponent_creature.speed > self.player_creature.speed:
            return self.opponent, self.player
        else:
            return random.sample([self.player, self.opponent], 2)

    def execute_skill(self, attacker, defender):
        if attacker == self.player:
            atk_creature = self.player_creature
            def_creature = self.opponent_creature
        else:
            atk_creature = self.opponent_creature
            def_creature = self.player_creature
            
        skill = self.queued_skills[attacker.uid]
        damage = atk_creature.attack + skill.base_damage - def_creature.defense
        def_creature.hp -= max(1, damage)
        
        self._show_text(self.player, f"{atk_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{atk_creature.display_name} used {skill.display_name}!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.opponent, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.opponent, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
