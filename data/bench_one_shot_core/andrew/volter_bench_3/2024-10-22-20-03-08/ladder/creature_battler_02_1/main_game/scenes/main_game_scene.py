from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        battle_ended = False
        while not battle_ended:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            # Check for battle end
            battle_ended = self._check_battle_end()

        # Transition back to the main menu after the battle ends
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [SelectThing(skill) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        if self.player_creature.speed >= self.opponent_creature.speed:
            first_attacker, second_attacker = self.player, self.opponent
            first_skill, second_skill = player_skill, foe_skill
        else:
            first_attacker, second_attacker = self.opponent, self.player
            first_skill, second_skill = foe_skill, player_skill

        self._execute_skill(first_attacker, first_skill)
        if not self._check_battle_end():
            self._execute_skill(second_attacker, second_skill)

    def _execute_skill(self, attacker: Player, skill: Skill):
        if attacker == self.player:
            attacker_creature, defender_creature = self.player_creature, self.opponent_creature
        else:
            attacker_creature, defender_creature = self.opponent_creature, self.player_creature

        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False
