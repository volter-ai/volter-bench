from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.foe_creature = self.foe.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.foe.display_name}'s {self.foe_creature.display_name}: HP {self.foe_creature.hp}/{self.foe_creature.max_hp}

Your skills:
{self._format_skills(self.player_creature.skills)}

Foe's skills:
{self._format_skills(self.foe_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.foe, self.foe_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            if self._check_battle_end():
                break

    def _player_choice_phase(self, player: Player, creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=f"{skill.display_name} (Damage: {skill.damage})") for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} uses {player_skill.display_name}!")
        self._show_text(self.foe, f"{self.foe.display_name}'s {self.foe_creature.display_name} uses {foe_skill.display_name}!")
        
        self.foe_creature.hp -= player_skill.damage
        self.player_creature.hp -= foe_skill.damage
        
        self._show_text(self.player, f"{self.foe.display_name}'s {self.foe_creature.display_name} takes {player_skill.damage} damage!")
        self._show_text(self.foe, f"{self.player.display_name}'s {self.player_creature.display_name} takes {foe_skill.damage} damage!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} has been defeated. You lose!")
            self._show_text(self.foe, f"You have defeated {self.player.display_name}'s {self.player_creature.display_name}. You win!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.foe_creature.hp <= 0:
            self._show_text(self.player, f"You have defeated {self.foe.display_name}'s {self.foe_creature.display_name}. You win!")
            self._show_text(self.foe, f"Your {self.foe_creature.display_name} has been defeated. You lose!")
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.foe_creature.hp = self.foe_creature.max_hp
