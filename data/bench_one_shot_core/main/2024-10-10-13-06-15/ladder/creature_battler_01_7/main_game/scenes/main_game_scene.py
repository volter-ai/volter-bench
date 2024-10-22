from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from collections import deque


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue = deque()

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
{self.get_skill_choices_str()}
"""

    def get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        self.battle_loop()
        self.display_battle_result()
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def battle_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            self.skill_queue.append((self.player, self.player_creature, player_skill))
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            self.skill_queue.append((self.foe, self.foe_creature, foe_skill))
            
            # Resolution Phase
            self.resolution_phase()
            
            # Check for battle end
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return choice.thing

    def resolution_phase(self):
        while self.skill_queue:
            attacker, attacker_creature, skill = self.skill_queue.popleft()
            defender = self.foe if attacker == self.player else self.player
            defender_creature = self.foe_creature if attacker == self.player else self.player_creature
            
            self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
            defender_creature.hp -= skill.damage
            defender_creature.hp = max(0, defender_creature.hp)

            if self.check_battle_end():
                break

    def check_battle_end(self):
        return self.player_creature.hp == 0 or self.foe_creature.hp == 0

    def display_battle_result(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lost the battle.")
        else:
            self._show_text(self.player, f"{self.foe_creature.display_name} fainted! You won the battle!")

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
