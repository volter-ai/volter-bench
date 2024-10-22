from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Available skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        
        while not self.battle_ended:
            # Player Choice Phase
            player_skill = self.player_turn()
            
            # Foe Choice Phase
            foe_skill = self.foe_turn()
            
            # Resolution Phase
            self.resolve_turn(player_skill, foe_skill)
            
            if self.check_battle_end():
                self.end_battle()

    def player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return choice.thing

    def resolve_turn(self, player_skill, foe_skill):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} used {player_skill.display_name}!")
        self.foe_creature.hp = max(0, self.foe_creature.hp - player_skill.damage)
        
        self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} used {foe_skill.display_name}!")
        self.player_creature.hp = max(0, self.player_creature.hp - foe_skill.damage)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.foe_creature.hp == 0:
            self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} fainted! You win!")
            return True
        return False

    def end_battle(self):
        self.battle_ended = True
        self.reset_creatures()
        self._show_text(self.player, "The battle has ended. Returning to the main menu.")
        self._transition_to_scene("MainMenuScene")

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
