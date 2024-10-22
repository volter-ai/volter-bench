from main_game.models import Creature, SkillQueue
from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue = SkillQueue(display_name="Skill Queue", prototype_id="skill_queue")

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Player's turn:
{self.get_skill_choices_str(self.player_creature)}
"""

    def get_skill_choices_str(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        while True:
            if self.battle_round():
                self.end_battle()
                break

    def battle_round(self) -> bool:
        self.skill_queue.skills.clear()
        self.player_choice_phase()
        self.foe_choice_phase()
        return self.resolution_phase()

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        skill = next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)
        self.skill_queue.skills.append(skill)

    def foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        skill = next(skill for skill in self.foe_creature.skills if skill.display_name == choice.display_name)
        self.skill_queue.skills.append(skill)

    def resolution_phase(self) -> bool:
        for skill in self.skill_queue.skills:
            if self.skill_queue.skills.index(skill) == 0:
                attacker, defender = self.player, self.foe
                attacker_creature, defender_creature = self.player_creature, self.foe_creature
            else:
                attacker, defender = self.foe, self.player
                attacker_creature, defender_creature = self.foe_creature, self.player_creature

            defender_creature.hp -= skill.damage
            self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")

            if defender_creature.hp <= 0:
                self._show_text(self.player, f"{attacker.display_name} wins!")
                return True

        return False

    def end_battle(self):
        self.reset_creatures()
        self._show_text(self.player, "The battle has ended. Returning to the main menu.")
        self._transition_to_scene("MainMenuScene")

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
