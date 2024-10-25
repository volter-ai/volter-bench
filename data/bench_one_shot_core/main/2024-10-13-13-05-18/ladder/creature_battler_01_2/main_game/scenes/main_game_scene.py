from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from collections import deque


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.skill_queue = deque()

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}

Queued skills:
{', '.join([skill.display_name for skill in self.skill_queue])}
"""

    def run(self):
        self._show_text(self.player, "A wild creature appears!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            # Player Choice Phase
            self.player_choice_phase()
            
            # Foe Choice Phase
            self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase()
            
            # Check for battle end
            if self.check_battle_end():
                break

        self.end_battle()

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append((self.player, choice.thing))
        self._show_text(self.player, f"{self.player.display_name} queued {choice.thing.display_name}")

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        self.skill_queue.append((self.bot, choice.thing))
        self._show_text(self.player, f"{self.bot.display_name} queued a skill")

    def resolution_phase(self):
        while self.skill_queue:
            acting_player, skill = self.skill_queue.popleft()
            if acting_player == self.player:
                target = self.bot_creature
                attacker = self.player_creature
            else:
                target = self.player_creature
                attacker = self.bot_creature
            
            self._show_text(self.player, f"{acting_player.display_name}'s {attacker.display_name} uses {skill.display_name}!")
            target.hp -= skill.damage
            self._show_text(self.player, f"{target.display_name} takes {skill.damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"{self.bot.display_name}'s {self.bot_creature.display_name} fainted! You win!")
            return True
        return False

    def end_battle(self):
        self.reset_creatures()
        
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        
        choice = self._wait_for_choice(self.player, choices)
        
        if play_again_button == choice:
            self._transition_to_scene("MainMenuScene")
        elif quit_button == choice:
            self._quit_whole_game()

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self.skill_queue.clear()
