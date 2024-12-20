from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_chosen_skill = None
        self.bot_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

VS

{self.bot.display_name}'s {self.bot_creature.display_name}:
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Type: {self.bot_creature.creature_type}

Available Skills:
{self._format_skills()}
"""

    def _format_skills(self):
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type)" 
                         for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self._handle_player_turn()
            
            # Bot choice phase
            self.bot_chosen_skill = self._handle_bot_turn()
            
            # Resolution phase
            self._resolve_turn()
            
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

    def _resolve_turn(self):
        # Determine order
        first = self.player
        second = self.bot
        first_skill = self.player_chosen_skill
        second_skill = self.bot_chosen_skill
        
        if self.bot_creature.speed > self.player_creature.speed or \
           (self.bot_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_skill, second_skill = second_skill, first_skill

        # Execute skills
        for attacker, defender, skill in [(first, second, first_skill), 
                                        (second, first, second_skill)]:
            if attacker == self.player:
                atk_creature = self.player_creature
                def_creature = self.bot_creature
            else:
                atk_creature = self.bot_creature
                def_creature = self.player_creature

            damage = self._calculate_damage(atk_creature, def_creature, skill)
            def_creature.hp = max(0, def_creature.hp - damage)
            
            self._show_text(self.player, 
                f"{atk_creature.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage to {def_creature.display_name}!")
            
            if def_creature.hp == 0:
                break

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
