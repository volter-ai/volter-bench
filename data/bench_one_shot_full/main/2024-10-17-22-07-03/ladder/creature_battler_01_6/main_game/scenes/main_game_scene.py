from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Player's turn:
{self._get_skill_choices_str(self.player_creature)}

Opponent's turn:
{self._get_skill_choices_str(self.opponent_creature)}
"""

    def _get_skill_choices_str(self, creature):
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.opponent, self.opponent_creature)

            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)

            if self._check_battle_end():
                self._reset_creatures()
                if not self._play_again():
                    break

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        self._apply_skill(self.player, player_skill, self.opponent_creature)
        if not self._check_battle_end():
            self._apply_skill(self.opponent, foe_skill, self.player_creature)

    def _apply_skill(self, attacker: Player, skill: Skill, target: Creature):
        target.hp = max(0, target.hp - skill.damage)
        self._show_text(self.player, f"{attacker.display_name}'s {skill.display_name} dealt {skill.damage} damage to {target.display_name}!")
        self._show_text(self.opponent, f"{attacker.display_name}'s {skill.display_name} dealt {skill.damage} damage to {target.display_name}!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def _play_again(self) -> bool:
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        
        self._show_text(self.player, "Do you want to play again?")
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            return True
        elif choice == quit_button:
            self._quit_whole_game()
        
        return False
