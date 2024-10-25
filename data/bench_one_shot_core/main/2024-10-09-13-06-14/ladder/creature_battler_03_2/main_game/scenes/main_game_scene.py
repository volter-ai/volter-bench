from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        self._show_text(self.opponent, "Battle start!")

        while not self.battle_ended:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            if self._check_battle_end():
                self._end_battle()

    def _player_choice_phase(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, foe_skill: Skill):
        if self.player_creature.speed >= self.opponent_creature.speed:
            self._execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature)
        else:
            self._execute_skill(self.opponent, self.opponent_creature, foe_skill, self.player, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender: Player, defender_creature: Creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self._get_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * weakness_factor)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"It dealt {final_damage} damage!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def _get_weakness_factor(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire" and creature_type == "leaf":
            return 2.0
        elif skill_type == "fire" and creature_type == "water":
            return 0.5
        elif skill_type == "water" and creature_type == "fire":
            return 2.0
        elif skill_type == "water" and creature_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and creature_type == "water":
            return 2.0
        elif skill_type == "leaf" and creature_type == "fire":
            return 0.5
        else:
            return 1.0

    def _check_battle_end(self) -> bool:
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def _end_battle(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
        
        self.battle_ended = True
        self._transition_to_scene("MainMenuScene")
