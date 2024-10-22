from mini_game_engine.engine.lib import (AbstractGameScene, AbstractPlayer,
                                         Button)


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

Player's turn: {'Yes' if not self.player_skill_queue else 'No'}
Foe's turn: {'Yes' if not self.foe_skill_queue else 'No'}

Available skills:
{self._get_available_skills_str()}
"""

    def _get_available_skills_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, "Battle start!")
        while True:
            if not self.player_skill_queue:
                self._player_choice_phase()
            if not self.foe_skill_queue:
                self._foe_choice_phase()
            self._resolution_phase()
            
            if self._check_battle_end():
                break

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        selected_skill = next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)
        self.player_skill_queue.append(selected_skill)

    def _foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.foe_creature.skills]
        choice = self._wait_for_choice(self.foe, choices)
        selected_skill = next(skill for skill in self.foe_creature.skills if skill.display_name == choice.display_name)
        self.foe_skill_queue.append(selected_skill)

    def _resolution_phase(self):
        if self.player_skill_queue and self.foe_skill_queue:
            player_skill = self.player_skill_queue.pop(0)
            foe_skill = self.foe_skill_queue.pop(0)
            
            self._resolve_skill(self.player, player_skill, self.foe_creature)
            if not self._check_battle_end():
                self._resolve_skill(self.foe, foe_skill, self.player_creature)

    def _resolve_skill(self, attacker: AbstractPlayer, skill, target_creature):
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.creatures[0].display_name} uses {skill.display_name}!")
        target_creature.hp = max(0, target_creature.hp - skill.damage)
        self._show_text(self.player, f"{target_creature.display_name} takes {skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
