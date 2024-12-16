from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None
        self.current_phase = "player_choice"

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Phase: {self.current_phase}

Available Skills:
{self._format_skills()}"""

    def _format_skills(self):
        if self.current_phase == "player_choice":
            return "\n".join(f"> {skill.display_name}" for skill in self.player_creature.skills)
        return ""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player choice phase
            self.current_phase = "player_choice"
            self.player_chosen_skill = self._wait_for_choice(
                self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent choice phase  
            self.current_phase = "opponent_choice"
            self.opponent_chosen_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution phase
            self.current_phase = "resolution"
            self._resolve_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def _resolve_turn(self):
        first, second = self._determine_order()
        self._execute_skill(first[0], first[1], first[2], first[3])
        if second[1].hp > 0:  # Only do second attack if target still alive
            self._execute_skill(second[0], second[1], second[2], second[3])

    def _determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent_creature, self.player_chosen_skill, self.player_creature), \
                   (self.opponent, self.player_creature, self.opponent_chosen_skill, self.opponent_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player_creature, self.opponent_chosen_skill, self.opponent_creature), \
                   (self.player, self.opponent_creature, self.player_chosen_skill, self.player_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.opponent_creature, self.player_chosen_skill, self.player_creature), \
                       (self.opponent, self.player_creature, self.opponent_chosen_skill, self.opponent_creature)
            else:
                return (self.opponent, self.player_creature, self.opponent_chosen_skill, self.opponent_creature), \
                       (self.player, self.opponent_creature, self.player_chosen_skill, self.player_creature)

    def _execute_skill(self, attacker, defender, skill, attacker_creature):
        # Calculate raw damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender.defense
        
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"Dealt {final_damage} damage!")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
