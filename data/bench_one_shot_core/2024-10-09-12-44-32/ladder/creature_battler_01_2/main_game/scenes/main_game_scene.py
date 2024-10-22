from collections import deque

from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.skill_queue = deque()

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Your skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appeared!")
        
        while True:
            self.player_choice_phase()
            self.bot_choice_phase()
            self.resolution_phase()
            
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.damage} damage)") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.skill_queue.append((self.player, choice.thing))

    def bot_choice_phase(self):
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.damage} damage)") for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        self.skill_queue.append((self.bot, choice.thing))

    def resolution_phase(self):
        while self.skill_queue:
            attacker, skill = self.skill_queue.popleft()
            if attacker == self.player:
                defender = self.bot
                attacker_creature = self.player_creature
                defender_creature = self.bot_creature
            else:
                defender = self.player
                attacker_creature = self.bot_creature
                defender_creature = self.player_creature

            self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
            defender_creature.hp -= skill.damage
            self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} took {skill.damage} damage!")

            if defender_creature.hp <= 0:
                break

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"The opponent's {self.bot_creature.display_name} fainted! You won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
