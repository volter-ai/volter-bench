from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = {}

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}"""

    def run(self):
        while True:
            # Player phase
            player_skill = self._handle_player_turn()
            
            # Bot phase
            bot_skill = self._handle_bot_turn()
            
            # Resolution phase
            self._resolve_turn(player_skill, bot_skill)
            
            # Check win condition
            if self._check_battle_end():
                self._reset_creatures()  # Reset creature states before ending
                self._quit_whole_game()

    def _handle_player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return self.player_creature.skills[choices.index(choice)]

    def _handle_bot_turn(self):
        choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return self.bot_creature.skills[choices.index(choice)]

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _resolve_turn(self, player_skill, bot_skill):
        # Determine order based on speed, with random resolution for ties
        if self.player_creature.speed == self.bot_creature.speed:
            # Random choice when speeds are equal
            if random.choice([True, False]):
                first, second = self.player_creature, self.bot_creature
                first_skill, second_skill = player_skill, bot_skill
            else:
                first, second = self.bot_creature, self.player_creature
                first_skill, second_skill = bot_skill, player_skill
        else:
            # Higher speed goes first
            if self.player_creature.speed > self.bot_creature.speed:
                first, second = self.player_creature, self.bot_creature
                first_skill, second_skill = player_skill, bot_skill
            else:
                first, second = self.bot_creature, self.player_creature
                first_skill, second_skill = bot_skill, player_skill
        
        # Execute skills
        for attacker, defender, skill in [(first, second, first_skill), (second, first, second_skill)]:
            if defender.hp <= 0:
                continue
                
            damage = self._calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"It dealt {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            return True
        return False

    def _reset_creatures(self):
        """Reset all creatures to their initial state"""
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
