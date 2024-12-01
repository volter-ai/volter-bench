from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

VS

{self.bot.display_name}'s {self.bot_creature.display_name}
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Type: {self.bot_creature.creature_type}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._handle_player_turn()
            
            # Bot choice phase
            bot_skill = self._handle_bot_turn()
            
            # Resolution phase
            self._resolve_turn(player_skill, bot_skill)
            
            # Check win condition
            if self._check_battle_end():
                self._quit_whole_game()

    def _handle_player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(s for s in self.player_creature.skills if s.display_name == choice.display_name)

    def _handle_bot_turn(self):
        choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return next(s for s in self.bot_creature.skills if s.display_name == choice.display_name)

    def _get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == creature_type:
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_multiplier)

    def _resolve_turn(self, player_skill, bot_skill):
        # Determine order based on speed, with random choice if speeds are equal
        if self.player_creature.speed == self.bot_creature.speed:
            # Random choice between player and bot creature when speeds are equal
            first = random.choice([self.player_creature, self.bot_creature])
        else:
            # Higher speed goes first
            first = self.player_creature if self.player_creature.speed > self.bot_creature.speed else self.bot_creature
            
        second = self.bot_creature if first == self.player_creature else self.player_creature
        first_skill = player_skill if first == self.player_creature else bot_skill
        second_skill = bot_skill if first == self.player_creature else player_skill

        # First attack
        damage = self._calculate_damage(first, second, first_skill)
        second.hp = max(0, second.hp - damage)
        self._show_text(self.player, f"{first.display_name} used {first_skill.display_name} for {damage} damage!")
        
        # Second attack if still alive
        if second.hp > 0:
            damage = self._calculate_damage(second, first, second_skill)
            first.hp = max(0, first.hp - damage)
            self._show_text(self.player, f"{second.display_name} used {second_skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            return True
        return False
