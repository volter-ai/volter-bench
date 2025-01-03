from mini_game_engine.engine.lib import AbstractGameScene, Button

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "A wild trainer appears!")
        
        while True:
            # Player turn
            player_skill = self._handle_turn(self.player, self.player_creature)
            
            # Bot turn
            bot_skill = self._handle_turn(self.bot, self.bot_creature)
            
            # Resolution phase
            self._resolve_skills(player_skill, bot_skill)
            
            # Check win conditions
            if self._check_battle_end():
                break

        # Reset creatures before leaving
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _handle_turn(self, current_player, creature):
        skill_choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, skill_choices)
        return creature.skills[skill_choices.index(choice)]

    def _resolve_skills(self, player_skill, bot_skill):
        # Apply damage
        self.bot_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name}!")
        
        if self.bot_creature.hp > 0:
            self.player_creature.hp -= bot_skill.damage
            self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {bot_skill.display_name}!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures(self):
        """Reset creatures to their original state"""
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
