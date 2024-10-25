from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
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
            # Player turn
            player_skill = self._player_turn()
            
            # Opponent turn
            opponent_skill = self._opponent_turn()
            
            # Resolve turns
            self._resolve_turns(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                self._reset_creatures()
                self._show_text(self.player, "The battle has ended.")
                choice = self._wait_for_choice(self.player, [
                    Button("Return to Main Menu"),
                    Button("Quit Game")
                ])
                if choice.display_name == "Return to Main Menu":
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
                break

    def _player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def _resolve_turns(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player_creature, player_skill, self.opponent_creature)
        else:
            # Random order when speeds are equal
            first, second = random.sample([
                (self.player_creature, player_skill),
                (self.opponent_creature, opponent_skill)
            ], 2)
            self._execute_skill(first[0], first[1], second[0])
            if second[0].hp > 0:
                self._execute_skill(second[0], second[1], first[0])

    def _execute_skill(self, attacker, skill, defender):
        damage = self._calculate_damage(attacker, skill, defender)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {defender.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, skill, defender):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
