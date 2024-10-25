from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            if self.player_choice_phase() and self.foe_choice_phase():
                if not self.resolution_phase():
                    self.handle_battle_end()
                    break
            else:
                self.handle_battle_end()
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = choice.thing
        return True

    def foe_choice_phase(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill = choice.thing
        return True

    def resolution_phase(self):
        if self.player_creature.speed >= self.opponent_creature.speed:
            first, second = self.player, self.opponent
            first_skill, second_skill = self.player_skill, self.opponent_skill
        else:
            first, second = self.opponent, self.player
            first_skill, second_skill = self.opponent_skill, self.player_skill

        if not self.execute_skill(first, second, first_skill):
            return False
        if not self.execute_skill(second, first, second_skill):
            return False
        return True

    def execute_skill(self, attacker, defender, skill):
        attacker_creature = attacker.creatures[0]
        defender_creature = defender.creatures[0]

        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} fainted!")
            if defender == self.player:
                self._show_text(self.player, "You lost the battle!")
            else:
                self._show_text(self.player, "You won the battle!")
            return False
        return True

    def calculate_weakness_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def handle_battle_end(self):
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        self._show_text(self.player, "Battle ended. What would you like to do?")
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
