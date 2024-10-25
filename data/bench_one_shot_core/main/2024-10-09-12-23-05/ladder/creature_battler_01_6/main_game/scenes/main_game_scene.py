from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.skill_queue = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self._show_text(self.opponent, f"You encountered {self.player.display_name}'s {self.player_creature.display_name}!")

        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append((self.player, choice.thing))

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.skill_queue.append((self.opponent, choice.thing))

    def resolution_phase(self):
        while self.skill_queue:
            acting_player, skill = self.skill_queue.pop(0)
            target_player = self.opponent if acting_player == self.player else self.player
            target_creature = self.opponent_creature if acting_player == self.player else self.player_creature

            self._show_text(acting_player, f"You used {skill.display_name}!")
            self._show_text(target_player, f"Opponent used {skill.display_name}!")

            target_creature.hp -= skill.damage
            target_creature.hp = max(0, target_creature.hp)  # Ensure HP doesn't go below 0

            self._show_text(acting_player, f"You dealt {skill.damage} damage!")
            self._show_text(target_player, f"You received {skill.damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
