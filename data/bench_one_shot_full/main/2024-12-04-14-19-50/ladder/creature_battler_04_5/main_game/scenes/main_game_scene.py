from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_queued_skill = None
        self.opponent_queued_skill = None

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Your turn!")
            self.player_queued_skill = self._get_skill_choice(self.player, self.player_creature)

            # Opponent choice phase
            self._show_text(self.opponent, "Your turn!")
            self.opponent_queued_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution phase
            self._resolve_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                multiplier = 2.0
            elif defender_creature.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                multiplier = 2.0
            elif defender_creature.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                multiplier = 2.0
            elif defender_creature.creature_type == "fire":
                multiplier = 0.5

        return int(raw_damage * multiplier)

    def _resolve_turn(self):
        # Determine order
        if self.opponent_creature.speed > self.player_creature.speed:
            self._execute_skill(self.opponent_creature, self.player_creature, self.opponent_queued_skill)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player_creature, self.opponent_creature, self.player_queued_skill)
        elif self.opponent_creature.speed < self.player_creature.speed:
            self._execute_skill(self.player_creature, self.opponent_creature, self.player_queued_skill)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent_creature, self.player_creature, self.opponent_queued_skill)
        else:
            # Equal speed - random order
            if random.random() < 0.5:
                self._execute_skill(self.player_creature, self.opponent_creature, self.player_queued_skill)
                if self.opponent_creature.hp > 0:
                    self._execute_skill(self.opponent_creature, self.player_creature, self.opponent_queued_skill)
            else:
                self._execute_skill(self.opponent_creature, self.player_creature, self.opponent_queued_skill)
                if self.player_creature.hp > 0:
                    self._execute_skill(self.player_creature, self.opponent_creature, self.player_queued_skill)

    def _execute_skill(self, attacker, defender, skill):
        damage = self._calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, 
            f"{attacker.display_name} used {skill.display_name}! "
            f"Dealt {damage} damage to {defender.display_name}!")
