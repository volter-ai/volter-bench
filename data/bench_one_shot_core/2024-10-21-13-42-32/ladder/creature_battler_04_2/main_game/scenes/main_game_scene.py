from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
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
        while True:
            # Player turn
            player_skill = self._player_turn()
            
            # Opponent turn
            opponent_skill = self._opponent_turn()
            
            # Resolve turn
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                break

        # Reset creature states before transitioning
        self._reset_creature_states()

    def _player_turn(self):
        self._show_text(self.player, "Your turn! Choose a skill:")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def _resolve_turn(self, player_skill, opponent_skill):
        first, second = self._determine_turn_order(player_skill, opponent_skill)
        self._execute_skill(*first)
        if self._check_battle_end():
            return
        self._execute_skill(*second)

    def _determine_turn_order(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, player_skill, self.opponent_creature), (self.opponent, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, opponent_skill, self.player_creature), (self.player, player_skill, self.opponent_creature)
        else:
            if random.random() < 0.5:
                return (self.player, player_skill, self.opponent_creature), (self.opponent, opponent_skill, self.player_creature)
            else:
                return (self.opponent, opponent_skill, self.player_creature), (self.player, player_skill, self.opponent_creature)

    def _execute_skill(self, attacker, skill, target):
        if skill.is_physical:
            raw_damage = float(attacker.creatures[0].attack + skill.base_damage - target.defense)
        else:
            raw_damage = float(attacker.creatures[0].sp_attack) / float(target.sp_defense) * float(skill.base_damage)

        weakness_factor = self._calculate_weakness_factor(skill.skill_type, target.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        target.hp = max(0, target.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{target.display_name} took {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type, target_type):
        weakness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5},
            "normal": {}  # Normal type is neither effective nor ineffective against any type
        }
        return weakness_chart.get(skill_type, {}).get(target_type, 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}, you have lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"Congratulations {self.player.display_name}, you have won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_creature_states(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
