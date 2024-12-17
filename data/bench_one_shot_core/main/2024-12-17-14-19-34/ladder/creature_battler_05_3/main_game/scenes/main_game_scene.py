from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
{"> Swap" if self.get_available_creatures(self.player) else ""}"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                effectiveness = 2.0
            elif defender_creature.creature_type == "water":
                effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                effectiveness = 2.0
            elif defender_creature.creature_type == "leaf":
                effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                effectiveness = 2.0
            elif defender_creature.creature_type == "fire":
                effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_fainted_creature(self, player):
        available = self.get_available_creatures(player)
        if not available:
            return False
        
        choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def run(self):
        while True:
            # Build choice list based on available options
            choices = [Button("Attack")]
            if self.get_available_creatures(self.player):
                choices.append(Button("Swap"))
            
            choice = self._wait_for_choice(self.player, choices)

            player_action = None
            if choice.display_name == "Attack":
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                player_action = ("attack", skill_choice.thing)
            else:
                creature_choices = [SelectThing(c) for c in self.get_available_creatures(self.player)]
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                player_action = ("swap", creature_choice.thing)

            # Bot turn
            bot_action = ("attack", self.bot.active_creature.skills[0])  # Simple bot just uses first skill

            # Resolution phase
            if player_action[0] == "swap":
                self.player.active_creature = player_action[1]
                damage = self.calculate_damage(self.bot.active_creature, self.player.active_creature, bot_action[1])
                self.player.active_creature.hp -= damage
            elif bot_action[0] == "swap":
                self.bot.active_creature = bot_action[1]
                damage = self.calculate_damage(self.player.active_creature, self.bot.active_creature, player_action[1])
                self.bot.active_creature.hp -= damage
            else:
                # Both chose attacks - check speed
                if self.player.active_creature.speed >= self.bot.active_creature.speed:
                    first, second = self.player, self.bot
                    first_action, second_action = player_action, bot_action
                else:
                    first, second = self.bot, self.player
                    first_action, second_action = bot_action, player_action

                # Execute first attack
                damage = self.calculate_damage(first.active_creature, second.active_creature, first_action[1])
                second.active_creature.hp -= damage

                # Execute second attack if creature still conscious
                if second.active_creature.hp > 0:
                    damage = self.calculate_damage(second.active_creature, first.active_creature, second_action[1])
                    first.active_creature.hp -= damage

            # Check for fainted creatures
            if self.player.active_creature.hp <= 0:
                if not self.handle_fainted_creature(self.player):
                    self._show_text(self.player, "You lost!")
                    break
            if self.bot.active_creature.hp <= 0:
                if not self.handle_fainted_creature(self.bot):
                    self._show_text(self.player, "You won!")
                    break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")
