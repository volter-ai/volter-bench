from mini_game_engine.engine.lib import AbstractGameScene, Button, RandomModeGracefulExit
from main_game.models import Player, Creature


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
{self.get_skill_choices_str(self.player_creature)}
"""

    def get_skill_choices_str(self, creature):
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        try:
            self.game_loop()
        except RandomModeGracefulExit:
            self.battle_ended = True
        finally:
            if self.battle_ended:
                self._transition_to_scene("MainMenuScene")

    def game_loop(self):
        while not self.battle_ended:
            # Player Choice Phase
            player_skill = self.choose_skill(self.player, self.player_creature)

            # Foe Choice Phase
            foe_skill = self.choose_skill(self.foe, self.foe_creature)

            # Resolution Phase
            self.resolve_skills(player_skill, foe_skill)

            if self.check_battle_end():
                self.battle_ended = True

        self.reset_creatures()

    def choose_skill(self, player: Player, creature: Creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def resolve_skills(self, player_skill, foe_skill):
        self.foe_creature.hp -= player_skill.damage
        self._show_text(self.player, f"{self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.foe, f"{self.player_creature.display_name} used {player_skill.display_name}!")

        if self.foe_creature.hp > 0:
            self.player_creature.hp -= foe_skill.damage
            self._show_text(self.player, f"{self.foe_creature.display_name} used {foe_skill.display_name}!")
            self._show_text(self.foe, f"{self.foe_creature.display_name} used {foe_skill.display_name}!")

    def check_battle_end(self):
        if self.foe_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")
            return True
        elif self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
