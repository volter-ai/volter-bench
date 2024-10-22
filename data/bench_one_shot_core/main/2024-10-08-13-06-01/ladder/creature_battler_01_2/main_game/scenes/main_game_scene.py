from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.player_skill_queue = []
        self.foe_skill_queue = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player Skills:
{self._format_skills(self.player_creature.skills)}

Foe Skills:
{self._format_skills(self.foe_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.foe, "Battle Start!")
        
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            
            if self.check_battle_end():
                self.end_battle()
                break

    def player_choice_phase(self):
        self._show_text(self.player, "Choose your skill:")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill_queue.append(choice.thing)

    def foe_choice_phase(self):
        self._show_text(self.foe, "Choose your skill:")
        choices = [SelectThing(skill) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        self.foe_skill_queue.append(choice.thing)

    def resolution_phase(self):
        player_skill = self.player_skill_queue.pop(0)
        foe_skill = self.foe_skill_queue.pop(0)

        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self._show_text(self.foe, f"Foe used {foe_skill.display_name}!")

        self.foe_creature.hp -= player_skill.damage
        self.player_creature.hp -= foe_skill.damage

        self._show_text(self.player, f"Dealt {player_skill.damage} damage to foe!")
        self._show_text(self.foe, f"Dealt {foe_skill.damage} damage to player!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0 or self.foe_creature.hp <= 0:
            return True
        return False

    def end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.foe, "You won the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.foe, "You lost the battle!")

        self.reset_creatures()
        self._show_text(self.player, "Returning to Main Menu...")
        self._transition_to_scene("MainMenuScene")

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
