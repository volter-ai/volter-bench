from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


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

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._foe_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(self.player, self.player_creature, player_skill,
                                   self.opponent, self.opponent_creature, foe_skill)
            
            # Check for battle end
            if self._check_battle_end():
                self._reset_creatures()
                # Transition back to the main menu
                self._transition_to_scene("MainMenuScene")
                return

    def _player_choice_phase(self, player, creature):
        self._show_text(player, f"Choose a skill for {creature.display_name}")
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self, opponent, creature):
        self._show_text(opponent, f"Choose a skill for {creature.display_name}")
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(opponent, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player1, creature1, skill1, player2, creature2, skill2):
        first, second = self._determine_order(creature1, creature2, skill1, skill2)
        
        self._execute_skill(first[0], first[1], second[1], first[2])
        if second[1].hp > 0:
            self._execute_skill(second[0], second[1], first[1], second[2])

    def _determine_order(self, creature1, creature2, skill1, skill2):
        if creature1.speed > creature2.speed:
            return (self.player, creature1, skill1), (self.opponent, creature2, skill2)
        elif creature2.speed > creature1.speed:
            return (self.opponent, creature2, skill2), (self.player, creature1, skill1)
        else:
            if random.random() < 0.5:
                return (self.player, creature1, skill1), (self.opponent, creature2, skill2)
            else:
                return (self.opponent, creature2, skill2), (self.player, creature1, skill1)

    def _execute_skill(self, attacker, attacker_creature, defender_creature, skill):
        damage = self._calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender_creature.display_name}")
        self._show_text(self.opponent, f"{attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender_creature.display_name}")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return final_damage

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 1, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 1, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 1}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
