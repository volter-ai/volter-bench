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
            if self.resolution_phase():
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.queued_skills[self.player.prototype_id] = choice.thing

    def opponent_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.queued_skills[self.opponent.prototype_id] = choice.thing

    def resolution_phase(self):
        # Determine order based on speed
        first = self.player
        second = self.opponent
        if self.opponent_creature.speed > self.player_creature.speed:
            first, second = second, first
        elif self.opponent_creature.speed == self.player_creature.speed:
            if random.random() < 0.5:
                first, second = second, first

        # Execute skills in order
        for attacker in [first, second]:
            defender = self.opponent if attacker == self.player else self.player
            attacker_creature = self.player_creature if attacker == self.player else self.opponent_creature
            defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
            
            skill = self.queued_skills[attacker.prototype_id]
            damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
            defender_creature.hp -= damage

            self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")
            self._show_text(self.opponent, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

            if defender_creature.hp <= 0:
                winner = attacker
                self._show_text(self.player, f"{winner.display_name} wins!")
                self._show_text(self.opponent, f"{winner.display_name} wins!")
                self._transition_to_scene("MainMenuScene")
                return True

        self.queued_skills.clear()
        return False
