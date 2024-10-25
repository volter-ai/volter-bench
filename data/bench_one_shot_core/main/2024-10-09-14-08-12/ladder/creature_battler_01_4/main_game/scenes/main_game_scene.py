from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
from typing import List


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_skill_queue: List[Skill] = []
        self.opponent_skill_queue: List[Skill] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            self._player_choice_phase(self.player, self.player_creature, self.player_skill_queue)
            
            # Foe Choice Phase
            self._player_choice_phase(self.opponent, self.opponent_creature, self.opponent_skill_queue)
            
            # Resolution Phase
            self._resolution_phase()
            
            if self._check_battle_end():
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, current_player: Player, current_creature: Creature, skill_queue: List[Skill]):
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        skill_queue.append(choice.thing)

    def _resolution_phase(self):
        player_skill = self.player_skill_queue.pop(0)
        opponent_skill = self.opponent_skill_queue.pop(0)

        self._show_text(self.player, f"{self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.opponent, f"{self.opponent_creature.display_name} used {opponent_skill.display_name}!")
        
        self.opponent_creature.hp -= player_skill.damage
        self.player_creature.hp -= opponent_skill.damage
        
        self._show_text(self.player, f"{self.opponent_creature.display_name} took {player_skill.damage} damage!")
        self._show_text(self.player, f"{self.player_creature.display_name} took {opponent_skill.damage} damage!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lost the battle.")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You won the battle!")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
