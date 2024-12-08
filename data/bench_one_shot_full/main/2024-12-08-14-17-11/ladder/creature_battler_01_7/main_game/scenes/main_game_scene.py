from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Skill
from typing import List, Tuple

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        # Initialize creatures with their max hp
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        
    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Queue Phase - Collect all actions before resolution
            skill_queue = self._collect_turn_actions()
            
            # Resolution Phase - Execute queued actions
            battle_ended = self._resolve_skill_queue(skill_queue)
            
            if battle_ended:
                # Reset creatures before transitioning out
                self.player_creature.hp = self.player_creature.max_hp
                self.bot_creature.hp = self.bot_creature.max_hp
                self._transition_to_scene("MainMenuScene")
                return

    def _collect_turn_actions(self) -> List[Tuple[Player, Skill, Player]]:
        """Collect skills from both players into a queue"""
        skill_queue = []
        
        # Player Choice Phase
        player_skill = self._get_skill_choice(self.player, self.player_creature)
        skill_queue.append((self.player, player_skill, self.bot))
        
        # Bot Choice Phase
        bot_skill = self._get_skill_choice(self.bot, self.bot_creature)
        skill_queue.append((self.bot, bot_skill, self.player))
        
        return skill_queue

    def _resolve_skill_queue(self, skill_queue: List[Tuple[Player, Skill, Player]]) -> bool:
        """Execute all queued skills and return whether battle ended"""
        for attacker, skill, defender in skill_queue:
            # Get the correct creatures for attacker/defender
            attacker_creature = self.player_creature if attacker == self.player else self.bot_creature
            defender_creature = self.bot_creature if defender == self.bot else self.player_creature
            
            # Show skill use to both players
            self._show_text(self.player, 
                f"{'Your' if attacker == self.player else 'Foe'} {attacker_creature.display_name} used {skill.display_name}!")
            self._show_text(self.bot,
                f"{'Your' if attacker == self.bot else 'Foe'} {attacker_creature.display_name} used {skill.display_name}!")
            
            # Apply damage
            defender_creature.hp -= skill.damage
            
            # Check for battle end
            if defender_creature.hp <= 0:
                if defender == self.player:
                    self._show_text(self.player, "You lost!")
                    self._show_text(self.bot, "You won!")
                else:
                    self._show_text(self.player, "You won!")
                    self._show_text(self.bot, "You lost!")
                return True
                
        return False

    def _get_skill_choice(self, player: Player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)
