from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_actions = []

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.bot, "Battle Start!")

        while True:
            # Player Choice Phase
            player_skill = self._handle_turn(self.player, self.player_creature)
            
            # Bot Choice Phase  
            bot_skill = self._handle_turn(self.bot, self.bot_creature)

            # Resolution Phase
            self._resolve_skills(player_skill, bot_skill)

            # Check win condition
            if self._check_battle_end():
                break

    def _handle_turn(self, current_player: Player, current_creature: Creature):
        choices = []
        for skill in current_creature.skills:
            choice = DictionaryChoice(skill.display_name)
            choice.value = {"skill": skill}
            choices.append(choice)
        
        result = self._wait_for_choice(current_player, choices)
        return result.value["skill"]

    def _resolve_skills(self, player_skill, bot_skill):
        # Apply player skill
        self.bot_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        self._show_text(self.bot, f"Opponent's {self.player_creature.display_name} used {player_skill.display_name}!")

        # Apply bot skill if still alive
        if self.bot_creature.hp > 0:
            self.player_creature.hp -= bot_skill.damage
            self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {bot_skill.display_name}!")
            self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {bot_skill.display_name}!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.bot, "You won!")
            # Reset creatures before transitioning
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.bot, "You lost!")
            # Reset creatures before transitioning
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene") 
            return True
        return False

    def _reset_creatures(self):
        """Reset all creatures to their max HP before leaving the scene"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
