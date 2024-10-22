import random

from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


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

Your turn:
{self.get_skill_choices_str()}
"""

    def get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            if self.check_battle_end():
                self.end_battle()
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, foe_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skills_in_order(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature, foe_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            self.execute_skills_in_order(self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature, player_skill)
        else:
            # Equal speed, randomly determine order
            if random.choice([True, False]):
                self.execute_skills_in_order(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature, foe_skill)
            else:
                self.execute_skills_in_order(self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature, player_skill)

    def execute_skills_in_order(self, first_player, first_creature, first_skill, second_player, second_creature, second_skill):
        self.execute_skill(first_player, first_creature, first_skill, second_creature)
        if second_creature.hp > 0:
            self.execute_skill(second_player, second_creature, second_skill, first_creature)

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted. You lost!")
        else:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} fainted. You won!")
        
        self._show_text(self.player, "Returning to the main menu...")
        self._transition_to_scene("MainMenuScene")
