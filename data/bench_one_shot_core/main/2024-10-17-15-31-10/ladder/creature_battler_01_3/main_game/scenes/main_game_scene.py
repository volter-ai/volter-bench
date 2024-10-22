from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

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
        while not self.battle_ended:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player)

            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.opponent)

            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)

            if self._check_battle_end():
                self.battle_ended = True

        self._reset_creatures()
        self._return_to_main_menu()

    def _player_choice_phase(self, current_player):
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_player.creatures[0].skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, foe_skill):
        self._apply_skill(self.player, player_skill, self.opponent_creature)
        if not self._check_battle_end():
            self._apply_skill(self.opponent, foe_skill, self.player_creature)

    def _apply_skill(self, attacker, skill, target):
        damage = skill.damage
        target.hp = max(0, target.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{target.display_name} took {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def _return_to_main_menu(self):
        self._show_text(self.player, "Returning to Main Menu...")
        self._transition_to_scene("MainMenuScene")
