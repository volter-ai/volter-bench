from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

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
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            if self._check_battle_end():
                break

        # Reset creatures' state before transitioning
        self._reset_creatures_state()

        # Transition back to the main menu
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [SelectThing(skill) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        self._apply_skill(self.player, player_skill, self.opponent_creature)
        self._apply_skill(self.opponent, foe_skill, self.player_creature)

    def _apply_skill(self, user: Player, skill: Skill, target: Creature):
        target.hp = max(0, target.hp - skill.damage)
        self._show_text(self.player, f"{user.display_name}'s {skill.display_name} deals {skill.damage} damage to {target.display_name}!")
        self._show_text(self.opponent, f"{user.display_name}'s {skill.display_name} deals {skill.damage} damage to {target.display_name}!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def _reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
        self._show_text(self.opponent, "All creatures have been restored to full health.")
