import random

from mini_game_engine.engine.lib import AbstractGameScene, Button


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

Your turn:
{self.get_skill_choices()}
"""

    def get_skill_choices(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            # Player turn
            player_skill = self.player_turn()
            
            # Opponent turn
            opponent_skill = self.opponent_turn()
            
            # Resolve turn
            self.resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self.check_battle_end():
                self._show_text(self.player, "Battle has ended. Returning to main menu.")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def resolve_turn(self, player_skill, opponent_skill):
        first, second = self.determine_turn_order(player_skill, opponent_skill)
        self.execute_skill(*first)
        if not self.check_battle_end():
            self.execute_skill(*second)

    def determine_turn_order(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature, player_skill, self.opponent_creature), (self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature, opponent_skill, self.player_creature), (self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            if random.choice([True, False]):
                return (self.player, self.player_creature, player_skill, self.opponent_creature), (self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            else:
                return (self.opponent, self.opponent_creature, opponent_skill, self.player_creature), (self.player, self.player_creature, player_skill, self.opponent_creature)

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        damage = self.calculate_damage(attacker_creature, skill, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}! It dealt {damage} damage.")

    def calculate_damage(self, attacker, skill, defender):
        if skill.is_physical:
            raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        else:
            raw_damage = (float(attacker.sp_attack) / float(defender.sp_defense)) * float(skill.base_damage)
        
        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = type_factor * raw_damage
        return max(1, int(final_damage))  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1.0)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
