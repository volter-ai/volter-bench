from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_skill = None
        self.bot_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}"""

    def run(self):
        self._show_text(self.player, f"A battle begins between {self.player_creature.display_name} and {self.bot_creature.display_name}!")
        
        while True:
            # Player choice phase
            skill_choices = {skill.display_name: skill for skill in self.player_creature.skills}
            choice = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )
            self.player_skill = skill_choices[choice.display_name]
            
            # Bot choice phase
            bot_skill_choices = {skill.display_name: skill for skill in self.bot_creature.skills}
            bot_choice = self._wait_for_choice(
                self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills]
            )
            self.bot_skill = bot_skill_choices[bot_choice.display_name]

            # Resolution phase
            first, second = self.determine_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                break
                
            self.execute_turn(second)
            
            if self.check_battle_end():
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.bot)
        elif self.player_creature.speed < self.bot_creature.speed:
            return (self.bot, self.player)
        else:
            return random.choice([(self.player, self.bot), (self.bot, self.player)])

    def execute_turn(self, acting_player):
        attacker = self.player_creature if acting_player == self.player else self.bot_creature
        defender = self.bot_creature if acting_player == self.player else self.player_creature
        skill = self.player_skill if acting_player == self.player else self.bot_skill

        damage = self.calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * factor)

    def get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
