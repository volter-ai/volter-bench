from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_skill = None
        self.bot_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            # Player phase
            self.player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            
            # Bot phase
            self.bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills])

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
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.player)
        else:
            return random.choice([(self.player, self.bot), (self.bot, self.player)])

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            if attacker == self.player:
                raw_damage = self.player_creature.attack + skill.base_damage - self.bot_creature.defense
            else:
                raw_damage = self.bot_creature.attack + skill.base_damage - self.player_creature.defense
        else:
            if attacker == self.player:
                raw_damage = (self.player_creature.sp_attack / self.bot_creature.sp_defense) * skill.base_damage
            else:
                raw_damage = (self.bot_creature.sp_attack / self.player_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        if attacker == self.player:
            defender_type = self.bot_creature.creature_type
        else:
            defender_type = self.player_creature.creature_type

        effectiveness = self.get_type_effectiveness(skill.skill_type, defender_type)
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
            skill = self.player_skill.thing
            damage = self.calculate_damage(attacker, self.bot, skill)
            self.bot_creature.hp -= damage
            self._show_text(self.player, f"{self.player_creature.display_name} used {skill.display_name} for {damage} damage!")
        else:
            skill = self.bot_skill.thing
            damage = self.calculate_damage(attacker, self.player, skill)
            self.player_creature.hp -= damage
            self._show_text(self.player, f"{self.bot_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
