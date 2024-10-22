from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.reset_creatures()

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self.game_loop()
        self._transition_to_scene("MainMenuScene")  # Return to main menu after battle

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase(self.player, self.player_creature)

            # Foe Choice Phase
            opponent_skill = self.player_choice_phase(self.opponent, self.opponent_creature)

            # Resolution Phase
            self.resolution_phase(player_skill, opponent_skill)

            # Check for battle end condition
            if self.check_battle_end():
                break

    def player_choice_phase(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        if self.player_creature.speed >= self.opponent_creature.speed:
            self.execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature)
        else:
            self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(damage, 0)  # Ensure damage is not negative
        defender_creature.hp = max(defender_creature.hp - damage, 0)  # Ensure HP doesn't go below 0
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
