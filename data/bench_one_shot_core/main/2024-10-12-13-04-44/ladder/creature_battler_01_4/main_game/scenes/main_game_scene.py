from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        
        while not self.battle_ended:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            self.check_battle_end()

        self.end_battle()

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, foe_skill):
        self._show_text(self.player, f"{self.player_creature.display_name} uses {player_skill.display_name}!")
        self.opponent_creature.hp = max(0, self.opponent_creature.hp - player_skill.damage)
        
        if self.opponent_creature.hp > 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} uses {foe_skill.display_name}!")
            self.player_creature.hp = max(0, self.player_creature.hp - foe_skill.damage)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            self.battle_ended = True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
            self.battle_ended = True

    def end_battle(self):
        self.reset_creatures()
        self._show_text(self.player, "The battle has ended. Returning to the main menu.")
        self._transition_to_scene("MainMenuScene")

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
