from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
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
                # Instead of breaking, transition back to menu
                self._transition_to_scene("MainMenuScene")
                return

    def _handle_player_turn(self):
        self._show_text(self.player, "Choose your skill!")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        return self._wait_for_choice(self.player, choices).thing

    def _handle_bot_turn(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        return self._wait_for_choice(self.bot, choices).thing

    def _resolve_turn(self, player_skill, bot_skill):
        # Determine order based on speed
        first = (self.player, self.player_creature, player_skill)
        second = (self.bot, self.bot_creature, bot_skill)
        
        if self.bot_creature.speed > self.player_creature.speed:
            first, second = second, first
        elif self.bot_creature.speed == self.player_creature.speed:
            if random.random() < 0.5:
                first, second = second, first

        # Execute skills in order
        for attacker, attacker_creature, skill in [first, second]:
            if attacker == self.player:
                defender = self.bot
                defender_creature = self.bot_creature
            else:
                defender = self.player
                defender_creature = self.player_creature

            damage = self._calculate_damage(skill, attacker_creature, defender_creature)
            defender_creature.hp = max(0, defender_creature.hp - damage)
            
            self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"Dealt {damage} damage!")
            
            if defender_creature.hp == 0:
                break

    def _calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        # Return final damage as integer
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

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
