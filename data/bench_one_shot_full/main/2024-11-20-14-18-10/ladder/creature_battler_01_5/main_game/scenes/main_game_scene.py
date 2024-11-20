from mini_game_engine.engine.lib import AbstractGameScene, Button

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
        # Reset creatures at start by setting hp to max_hp
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.damage} damage" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A battle begins between {self.player.display_name} and {self.opponent.display_name}!")
        
        while True:
            # Player Choice Phase
            player_skill = self._handle_turn(self.player, self.player_creature)
            
            # Opponent Choice Phase  
            opponent_skill = self._handle_turn(self.opponent, self.opponent_creature)

            # Resolution Phase
            self._resolve_skills(player_skill, opponent_skill)
            
            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")

    def _handle_turn(self, current_player, creature):
        skill_choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, skill_choices)
        return creature.skills[skill_choices.index(choice)]

    def _resolve_skills(self, player_skill, opponent_skill):
        # Apply damage
        self.opponent_creature.hp -= player_skill.damage
        self.player_creature.hp -= opponent_skill.damage
        
        self._show_text(self.player, 
            f"Your {self.player_creature.display_name} used {player_skill.display_name}!\n"
            f"Opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name}!")
