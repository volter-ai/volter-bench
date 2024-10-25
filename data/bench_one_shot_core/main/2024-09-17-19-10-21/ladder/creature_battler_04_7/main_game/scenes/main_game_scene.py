from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Player's turn:
> {self.player_creature.skills[0].display_name}
> {self.player_creature.skills[1].display_name}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player turn
            player_skill = self._player_turn()
            
            # Opponent turn
            opponent_skill = self._opponent_turn()
            
            # Resolve turn
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                if self._play_again():
                    self._transition_to_scene("MainGameScene")
                else:
                    self._transition_to_scene("MainMenuScene")
                return

    def _player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed >= self.opponent_creature.speed:
            self._execute_skill(self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
        else:
            self._execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player_creature, player_skill, self.opponent_creature)

    def _execute_skill(self, attacker, skill, defender):
        damage = self._calculate_damage(attacker, skill, defender)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, skill, defender):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _play_again(self):
        play_again_button = Button("Play Again")
        main_menu_button = Button("Main Menu")
        choices = [play_again_button, main_menu_button]
        choice = self._wait_for_choice(self.player, choices)
        return choice == play_again_button
