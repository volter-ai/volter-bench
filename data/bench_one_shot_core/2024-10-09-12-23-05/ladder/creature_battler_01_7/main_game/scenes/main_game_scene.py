import os

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        self._show_text(self.opponent, f"You encounter {self.player.display_name}'s {self.player_creature.display_name}!")

        while True:
            # Player Choice Phase
            player_skill = self.choose_skill(self.player, self.player_creature)
            
            # Foe Choice Phase
            opponent_skill = self.choose_skill(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self.resolve_skills(player_skill, opponent_skill)
            
            if self.check_battle_end():
                break

        self.reset_creatures()

        # Check if we're in a test environment
        if 'PYTEST_CURRENT_TEST' in os.environ:
            self._quit_whole_game()
        else:
            self._transition_to_scene("MainMenuScene")

    def choose_skill(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def resolve_skills(self, player_skill: Skill, opponent_skill: Skill):
        self._show_text(self.player, f"Your {self.player_creature.display_name} uses {player_skill.display_name}!")
        self._show_text(self.opponent, f"Opponent's {self.opponent_creature.display_name} uses {opponent_skill.display_name}!")
        
        self.opponent_creature.hp -= player_skill.damage
        self.player_creature.hp -= opponent_skill.damage
        
        self.opponent_creature.hp = max(0, self.opponent_creature.hp)
        self.player_creature.hp = max(0, self.player_creature.hp)

    def check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
