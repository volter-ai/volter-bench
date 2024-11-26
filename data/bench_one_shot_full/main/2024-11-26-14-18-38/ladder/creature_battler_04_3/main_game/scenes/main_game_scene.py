from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creature stats
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}"""

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._get_player_choice()
            
            # Bot choice phase
            bot_skill = self._get_bot_choice()
            
            # Resolution phase
            self._resolve_turn(player_skill, bot_skill)
            
            # Check win condition
            if self._check_battle_end():
                break

    def _get_player_choice(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _get_bot_choice(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return choice.thing

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
        # Determine order
        first = self.player_creature if self.player_creature.speed > self.bot_creature.speed else self.bot_creature
        second = self.bot_creature if first == self.player_creature else self.player_creature
        first_skill = player_skill if first == self.player_creature else bot_skill
        second_skill = bot_skill if first == self.player_creature else player_skill
        
        # If speeds are equal, randomize
        if self.player_creature.speed == self.bot_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                first_skill, second_skill = second_skill, first_skill

        # Execute first attack
        if first == self.player_creature:
            damage = self._calculate_damage(self.player_creature, self.bot_creature, first_skill)
            self.bot_creature.hp = max(0, self.bot_creature.hp - damage)
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        else:
            damage = self._calculate_damage(self.bot_creature, self.player_creature, first_skill)
            self.player_creature.hp = max(0, self.player_creature.hp - damage)
            self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {first_skill.display_name} for {damage} damage!")

        # Check if battle should continue
        if self.player_creature.hp > 0 and self.bot_creature.hp > 0:
            # Execute second attack
            if second == self.player_creature:
                damage = self._calculate_damage(self.player_creature, self.bot_creature, second_skill)
                self.bot_creature.hp = max(0, self.bot_creature.hp - damage)
                self._show_text(self.player, f"Your {self.player_creature.display_name} used {second_skill.display_name} for {damage} damage!")
            else:
                damage = self._calculate_damage(self.bot_creature, self.player_creature, second_skill)
                self.player_creature.hp = max(0, self.player_creature.hp - damage)
                self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
