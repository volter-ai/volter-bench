import random
from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        
        while True:
            # Player Choice Phase
            player_skill = self._player_turn()
            
            # Foe Choice Phase
            foe_skill = self._foe_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, foe_skill)
            
            if self._check_battle_end():
                self._handle_battle_end()
                break

    def _player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_turn(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _determine_execution_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return [(self.player.prototype_id, self.player_creature), (self.opponent.prototype_id, self.opponent_creature)]
        elif self.player_creature.speed < self.opponent_creature.speed:
            return [(self.opponent.prototype_id, self.opponent_creature), (self.player.prototype_id, self.player_creature)]
        else:
            order = [(self.player.prototype_id, self.player_creature), (self.opponent.prototype_id, self.opponent_creature)]
            random.shuffle(order)
            return order

    def _resolve_turn(self, player_skill, foe_skill):
        execution_order = self._determine_execution_order()
        skills = [(self.player.prototype_id, player_skill), (self.opponent.prototype_id, foe_skill)]

        for attacker_id, attacker_creature in execution_order:
            defender_id, defender_creature = next((p_id, c) for p_id, c in execution_order if p_id != attacker_id)
            attacker_skill = next(skill for p_id, skill in skills if p_id == attacker_id)
            attacker = self.player if attacker_id == self.player.prototype_id else self.opponent
            self._execute_skill(attacker, attacker_creature, attacker_skill, defender_creature)
            if defender_creature.hp <= 0:
                break

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(1, damage)  # Ensure at least 1 damage is dealt
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} takes {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False

    def _handle_battle_end(self):
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            self._transition_to_scene("MainMenuScene")
        elif choice == quit_button:
            self._quit_whole_game()
