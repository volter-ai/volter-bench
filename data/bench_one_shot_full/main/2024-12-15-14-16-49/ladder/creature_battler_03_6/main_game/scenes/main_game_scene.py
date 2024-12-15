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
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

{self.bot.display_name}'s {self.bot_creature.display_name}:
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
                # Return to main menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return

    def _handle_player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills 
                   if skill.display_name == choice.display_name)

    def _handle_bot_turn(self):
        choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return next(skill for skill in self.bot_creature.skills 
                   if skill.display_name == choice.display_name)

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _resolve_turn(self, player_skill, bot_skill):
        # Determine order based on speed
        if self.player_creature.speed > self.bot_creature.speed:
            first, second = (self.player_creature, player_skill), (self.bot_creature, bot_skill)
        elif self.bot_creature.speed > self.player_creature.speed:
            first, second = (self.bot_creature, bot_skill), (self.player_creature, player_skill)
        else:
            if random.random() < 0.5:
                first, second = (self.player_creature, player_skill), (self.bot_creature, bot_skill)
            else:
                first, second = (self.bot_creature, bot_skill), (self.player_creature, player_skill)

        # Execute attacks
        for attacker, skill in [first, second]:
            if attacker == self.player_creature:
                damage = self._calculate_damage(attacker, self.bot_creature, skill)
                self.bot_creature.hp -= damage
                self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
            else:
                damage = self._calculate_damage(attacker, self.player_creature, skill)
                self.player_creature.hp -= damage
                self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

            if self._check_battle_end():
                break

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
