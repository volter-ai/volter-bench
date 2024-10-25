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
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_turn()
            
            # Foe Choice Phase
            foe_skill = self.opponent_turn()
            
            # Resolution Phase
            self.resolve_turn(player_skill, foe_skill)
            
            # Check for battle end
            if self.check_battle_end():
                self.reset_creatures()
                self._show_text(self.player, "Returning to Main Menu...")
                self._transition_to_scene("MainMenuScene")
                return

    def player_turn(self):
        self._show_text(self.player, "Choose your skill:")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolve_turn(self, player_skill, foe_skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self.opponent_creature.hp = max(0, self.opponent_creature.hp - player_skill.damage)
        self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} took {player_skill.damage} damage!")

        self._show_text(self.player, f"Opponent used {foe_skill.display_name}!")
        self.player_creature.hp = max(0, self.player_creature.hp - foe_skill.damage)
        self._show_text(self.player, f"Your {self.player_creature.display_name} took {foe_skill.damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
