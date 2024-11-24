from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
from typing import NamedTuple

class QueuedSkill(NamedTuple):
    skill: 'Skill'
    user: 'Creature'
    target: 'Creature'

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.skill_queue: list[QueuedSkill] = []

    def __str__(self):
        queue_str = "\nQueued Actions:"
        if self.skill_queue:
            for queued in self.skill_queue:
                queue_str += f"\n> {queued.user.display_name} will use {queued.skill.display_name} on {queued.target.display_name}"
        else:
            queue_str += "\n> No actions queued"
            
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
{queue_str}
"""

    def run(self):
        self._show_text(self.player, "A wild creature appears!")
        
        while True:
            # Clear queue at start of turn
            self.skill_queue.clear()
            
            # Player Choice Phase
            self._player_choice_phase()
            
            # Foe Choice Phase
            self._foe_choice_phase()
            
            # Resolution Phase
            self._resolution_phase()
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self):
        """Player Choice Phase - Queue player's chosen skill"""
        choices = [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills]
        for choice, skill in zip(choices, self.player_creature.skills):
            choice.value = {"skill": skill}
        
        choice = self._wait_for_choice(self.player, choices)
        chosen_skill = choice.value["skill"]
        
        self.skill_queue.append(QueuedSkill(
            skill=chosen_skill,
            user=self.player_creature,
            target=self.bot_creature
        ))
        self._show_text(self.player, f"You chose {chosen_skill.display_name}!")

    def _foe_choice_phase(self):
        """Foe Choice Phase - Queue bot's chosen skill"""
        choices = [DictionaryChoice(skill.display_name) for skill in self.bot_creature.skills]
        for choice, skill in zip(choices, self.bot_creature.skills):
            choice.value = {"skill": skill}
        
        choice = self._wait_for_choice(self.bot, choices)
        chosen_skill = choice.value["skill"]
        
        self.skill_queue.append(QueuedSkill(
            skill=chosen_skill,
            user=self.bot_creature,
            target=self.player_creature
        ))
        self._show_text(self.player, f"Foe chose {chosen_skill.display_name}!")

    def _resolution_phase(self):
        """Resolution Phase - Resolve all queued skills"""
        self._show_text(self.player, "=== Resolution Phase ===")
        
        while self.skill_queue:
            queued = self.skill_queue.pop(0)
            queued.target.hp -= queued.skill.damage
            self._show_text(self.player, 
                f"{queued.user.display_name} used {queued.skill.display_name} on {queued.target.display_name}!")
