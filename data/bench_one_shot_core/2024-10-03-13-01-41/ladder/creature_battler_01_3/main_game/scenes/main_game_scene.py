from collections import deque

from main_game.models import Creature, Player
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.queue = deque()

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

Foe's skills:
{self._format_skills(self.foe_creature.skills)}

Skills in queue: {len(self.queue)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            self.player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            self.player_choice_phase(self.foe, self.foe_creature)

            # Resolution Phase
            self.resolution_phase()

            # Check for battle end
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._show_text(self.player, "Returning to the main menu...")
        self._show_text(self.foe, "Returning to the main menu...")
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, player: Player, creature: Creature):
        choices = [SelectThing(skill, label=f"Use {skill.display_name}") for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        self.queue.append((player, choice.thing))

    def resolution_phase(self):
        while self.queue:
            player, skill = self.queue.popleft()
            target = self.foe_creature if player == self.player else self.player_creature
            self._show_text(self.player, f"{player.display_name}'s {player.creatures[0].display_name} uses {skill.display_name}!")
            self._show_text(self.foe, f"{player.display_name}'s {player.creatures[0].display_name} uses {skill.display_name}!")
            target.hp -= skill.damage
            target.hp = max(0, target.hp)

    def check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} was defeated. You lose!")
            self._show_text(self.foe, f"You defeated {self.player.display_name}'s {self.player_creature.display_name}. You win!")
            return True
        elif self.foe_creature.hp == 0:
            self._show_text(self.player, f"You defeated {self.foe.display_name}'s {self.foe_creature.display_name}. You win!")
            self._show_text(self.foe, f"Your {self.foe_creature.display_name} was defeated. You lose!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
        self.queue.clear()
