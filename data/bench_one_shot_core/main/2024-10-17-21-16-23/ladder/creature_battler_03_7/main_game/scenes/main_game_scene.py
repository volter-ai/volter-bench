from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        if self.battle_ended:
            return """===Battle Ended===
> Return to Main Menu
> Quit Game
"""
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Available skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            if not self.battle_ended:
                # Player Choice Phase
                player_skill = self._player_turn()
                
                # Foe Choice Phase
                foe_skill = self._foe_turn()
                
                # Resolution Phase
                self._resolve_turn(player_skill, foe_skill)
                
                if self._check_battle_end():
                    self.battle_ended = True
            else:
                # Battle has ended, ask player for next action
                choice = self._wait_for_choice(self.player, [
                    Button("Return to Main Menu"),
                    Button("Quit Game")
                ])
                
                if choice.display_name == "Return to Main Menu":
                    self._transition_to_scene("MainMenuScene")
                    return
                elif choice.display_name == "Quit Game":
                    self._quit_whole_game()
                    return

    def _player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _foe_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolve_turn(self, player_skill, foe_skill):
        first, second = self._determine_order(self.player_creature, self.opponent_creature)
        
        if first == self.player_creature:
            self._execute_skill(self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent_creature, foe_skill, self.player_creature)
        else:
            self._execute_skill(self.opponent_creature, foe_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player_creature, player_skill, self.opponent_creature)

    def _determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def _execute_skill(self, attacker, skill, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        factor = self._get_weakness_resistance_factor(skill.skill_type, defender.creature_type)
        final_damage = int(factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def _get_weakness_resistance_factor(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1
        elif skill_type == "fire" and creature_type == "leaf":
            return 2
        elif skill_type == "fire" and creature_type == "water":
            return 0.5
        elif skill_type == "water" and creature_type == "fire":
            return 2
        elif skill_type == "water" and creature_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and creature_type == "water":
            return 2
        elif skill_type == "leaf" and creature_type == "fire":
            return 0.5
        else:
            return 1

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
