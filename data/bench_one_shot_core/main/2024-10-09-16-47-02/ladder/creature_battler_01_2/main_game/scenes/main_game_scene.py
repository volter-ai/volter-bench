from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            self.skill_queue.append((self.player_creature, self.foe_creature, player_skill))
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            self.skill_queue.append((self.foe_creature, self.player_creature, foe_skill))
            
            # Resolution Phase
            self.resolution_phase()
            
            # Check for battle end
            if self.check_battle_end():
                break
        
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        return choice.thing

    def resolution_phase(self):
        while self.skill_queue:
            attacker, defender, skill = self.skill_queue.pop(0)
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
            defender.hp -= skill.damage
            defender.hp = max(0, defender.hp)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.foe_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.foe.creatures:
            creature.hp = creature.max_hp
