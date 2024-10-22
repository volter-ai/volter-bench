from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

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
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        
        battle_ended = False
        while not battle_ended:
            # Player turn
            player_skill = self._player_turn()
            
            # Opponent turn
            opponent_skill = self._opponent_turn()
            
            # Resolution phase
            self._resolve_turn(player_skill, opponent_skill)
            
            battle_ended = self._check_battle_end()

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_turn(self):
        self._show_text(self.player, "Your turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        self._show_text(self.opponent, "Opponent's turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolve_turn(self, player_skill, opponent_skill):
        self._apply_damage(self.player, player_skill, self.opponent_creature)
        if not self._check_battle_end():
            self._apply_damage(self.opponent, opponent_skill, self.player_creature)

    def _apply_damage(self, attacker, skill, target):
        target.hp = max(0, target.hp - skill.damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{target.display_name} took {skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
