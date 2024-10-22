from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
from typing import List, Tuple


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.foe_creature = self.foe.creatures[0]
        self.skill_queue: List[Tuple[Player, Skill]] = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.foe_creature.display_name} appeared!")
        
        battle_ended = False
        while not battle_ended:
            # Clear the skill queue at the start of each turn
            self.skill_queue.clear()

            # Player Choice Phase
            self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            self._player_choice_phase(self.foe, self.foe_creature)
            
            # Resolution Phase
            self._resolution_phase()
            
            # Check for battle end
            battle_ended = self._check_battle_end()

        self._reset_creatures()
        
        # After the battle ends, show options to play again or return to main menu
        self._show_text(self.player, "What would you like to do next?")
        play_again_button = Button("Play Again")
        main_menu_button = Button("Return to Main Menu")
        choices = [play_again_button, main_menu_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            self._transition_to_scene("MainGameScene")
        else:
            self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, current_player: Player, current_creature: Creature):
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        chosen_skill = choice.thing
        self.skill_queue.append((current_player, chosen_skill))

    def _resolution_phase(self):
        while self.skill_queue:
            attacker, skill = self.skill_queue.pop(0)
            if attacker == self.player:
                target = self.foe_creature
            else:
                target = self.player_creature
            self._apply_damage(attacker, skill, target)
            if self._check_battle_end():
                break

    def _apply_damage(self, attacker: Player, skill: Skill, target: Creature):
        damage = skill.damage
        target.hp = max(0, target.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {skill.display_name} dealt {damage} damage to {target.display_name}!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted. You lost!")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, f"The wild {self.foe_creature.display_name} fainted. You won!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
