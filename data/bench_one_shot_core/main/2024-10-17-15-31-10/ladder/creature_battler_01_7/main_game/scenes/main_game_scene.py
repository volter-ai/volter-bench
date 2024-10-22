from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.max_turns = 20  # Add a maximum number of turns to prevent infinite loops

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self._show_text(self.opponent, f"A wild {self.player_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        turn_count = 0
        while turn_count < self.max_turns:
            player_skill = self.player_turn()
            opponent_skill = self.opponent_turn()
            self.resolve_turn(player_skill, opponent_skill)
            
            if self.check_battle_end():
                self.end_battle()
                return
            
            turn_count += 1

        self._show_text(self.player, "The battle has reached a stalemate!")
        self._show_text(self.opponent, "The battle has reached a stalemate!")
        self.end_battle()

    def player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolve_turn(self, player_skill: Skill, opponent_skill: Skill):
        self._show_text(self.player, f"You used {player_skill.display_name}!")
        self._show_text(self.opponent, f"Opponent used {opponent_skill.display_name}!")
        
        self.opponent_creature.hp = max(0, self.opponent_creature.hp - player_skill.damage)
        self.player_creature.hp = max(0, self.player_creature.hp - opponent_skill.damage)
        
        self._show_text(self.player, f"You dealt {player_skill.damage} damage!")
        self._show_text(self.opponent, f"Opponent dealt {opponent_skill.damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def end_battle(self):
        self._show_text(self.player, "Resetting creatures and returning to main menu...")
        self._show_text(self.opponent, "Resetting creatures and returning to main menu...")
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")
