from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.skill_queue: List[tuple[Player, Creature, Skill]] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

> Use Skill
> Quit
"""

    def _format_skills(self, skills):
        return "\n".join([f"- {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        
        while True:
            # Player turn
            use_skill_button = Button("Use Skill")
            quit_button = Button("Quit")
            choice = self._wait_for_choice(self.player, [use_skill_button, quit_button])

            if quit_button == choice:
                self._quit_whole_game()

            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_skill = self._wait_for_choice(self.player, skill_choices).thing
            self.skill_queue.append((self.player, self.player_creature, player_skill))

            # Opponent turn
            opponent_skill = self._wait_for_choice(self.opponent, [SelectThing(skill) for skill in self.opponent_creature.skills]).thing
            self.skill_queue.append((self.opponent, self.opponent_creature, opponent_skill))

            # Resolution phase
            self._resolve_turn()
            if self._check_battle_end():
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _resolve_turn(self):
        while self.skill_queue:
            attacker, attacker_creature, skill = self.skill_queue.pop(0)
            defender = self.opponent if attacker == self.player else self.player
            defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
            
            damage = skill.damage
            defender_creature.hp = max(0, defender_creature.hp - damage)
            self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} uses {skill.display_name}!")
            self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} takes {damage} damage!")
            
            if self._check_battle_end():
                break

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted. You lose!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted. You win!")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
