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
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.bot.display_name}'s {self.bot_creature.display_name} (HP: {self.bot_creature.hp}/{self.bot_creature.max_hp})

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            
            # Create buttons that match skill names
            skill_buttons = [Button(skill.display_name) for skill in self.player_creature.skills]
            chosen_button = self._wait_for_choice(self.player, skill_buttons)
            
            # Map the chosen button back to the actual skill
            self.player_chosen_skill = next(
                skill for skill in self.player_creature.skills 
                if skill.display_name == chosen_button.display_name
            )

            # Bot choice phase
            bot_skill_buttons = [Button(skill.display_name) for skill in self.bot_creature.skills]
            chosen_bot_button = self._wait_for_choice(self.bot, bot_skill_buttons)
            
            # Map the chosen button back to the actual skill
            self.bot_chosen_skill = next(
                skill for skill in self.bot_creature.skills 
                if skill.display_name == chosen_bot_button.display_name
            )

            # Resolution phase
            first, second = self.determine_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                break
                
            self.execute_turn(second)
            
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.bot)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.player)
        else:
            return random.choice([(self.player, self.bot), (self.bot, self.player)])

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def execute_turn(self, attacker):
        if attacker == self.player:
            damage = self.calculate_damage(self.player_creature, self.bot_creature, self.player_chosen_skill)
            self.bot_creature.hp = max(0, self.bot_creature.hp - damage)
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {self.player_chosen_skill.display_name} for {damage} damage!")
            self._show_text(self.bot, f"Opponent's {self.player_creature.display_name} used {self.player_chosen_skill.display_name} for {damage} damage!")
        else:
            damage = self.calculate_damage(self.bot_creature, self.player_creature, self.bot_chosen_skill)
            self.player_creature.hp = max(0, self.player_creature.hp - damage)
            self._show_text(self.player, f"Opponent's {self.bot_creature.display_name} used {self.bot_chosen_skill.display_name} for {damage} damage!")
            self._show_text(self.bot, f"Your {self.bot_creature.display_name} used {self.bot_chosen_skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.bot, "You won!")
            # Reset creatures before transitioning
            self.player_creature.hp = self.player_creature.max_hp
            self.bot_creature.hp = self.bot_creature.max_hp
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.bot, "You lost!")
            # Reset creatures before transitioning
            self.player_creature.hp = self.player_creature.max_hp
            self.bot_creature.hp = self.bot_creature.max_hp
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
