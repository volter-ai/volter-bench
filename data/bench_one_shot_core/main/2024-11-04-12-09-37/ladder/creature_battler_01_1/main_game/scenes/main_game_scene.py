from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_skill_queue = []
        self.bot_skill_queue = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

Opponent's skills:
{self._format_skills(self.bot_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            # Player Choice Phase
            self._player_choice_phase()
            
            # Foe Choice Phase
            self._foe_choice_phase()
            
            # Resolution Phase
            self._resolution_phase()
            
            # Check for battle end
            if self._check_battle_end():
                self._reset_creature_state()
                break

    def _player_choice_phase(self):
        self._show_text(self.player, "Your turn!")
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        skill = next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)
        self.player_skill_queue.append(skill)

    def _foe_choice_phase(self):
        self._show_text(self.bot, "Opponent's turn!")
        choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        skill = next(skill for skill in self.bot_creature.skills if skill.display_name == choice.display_name)
        self.bot_skill_queue.append(skill)

    def _resolution_phase(self):
        while self.player_skill_queue or self.bot_skill_queue:
            if self.player_skill_queue:
                player_skill = self.player_skill_queue.pop(0)
                self.bot_creature.hp -= player_skill.damage
                self._show_text(self.player, f"You used {player_skill.display_name}! It dealt {player_skill.damage} damage.")
            
            if self.bot_skill_queue:
                bot_skill = self.bot_skill_queue.pop(0)
                self.player_creature.hp -= bot_skill.damage
                self._show_text(self.player, f"Opponent used {bot_skill.display_name}! It dealt {bot_skill.damage} damage.")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creature_state(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self.player_skill_queue.clear()
        self.bot_skill_queue.clear()
