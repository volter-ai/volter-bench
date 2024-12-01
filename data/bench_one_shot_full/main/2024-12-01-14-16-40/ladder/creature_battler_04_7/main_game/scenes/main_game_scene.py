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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player turn
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Determine order
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )
            
            # Execute turns
            for attacker, defender in [first, second]:
                player, creature, skill = attacker
                target_player, target_creature = defender
                
                damage = self._calculate_damage(skill, creature, target_creature)
                target_creature.hp = max(0, target_creature.hp - damage)
                
                self._show_text(player, f"{creature.display_name} used {skill.display_name}!")
                self._show_text(player, f"Dealt {damage} damage!")
                
                if target_creature.hp <= 0:
                    winner = "You" if target_creature == self.bot_creature else "Bot"
                    self._show_text(self.player, f"{winner} won!")
                    self._reset_creatures()
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_order(self, player_data, bot_data):
        player_creature = player_data[1]
        bot_creature = bot_data[1]
        
        if player_creature.speed > bot_creature.speed:
            return (player_data, (self.bot, self.bot_creature)), (bot_data, (self.player, self.player_creature))
        elif player_creature.speed < bot_creature.speed:
            return (bot_data, (self.player, self.player_creature)), (player_data, (self.bot, self.bot_creature))
        else:
            if random.random() < 0.5:
                return (player_data, (self.bot, self.bot_creature)), (bot_data, (self.player, self.player_creature))
            return (bot_data, (self.player, self.player_creature)), (player_data, (self.bot, self.bot_creature))

    def _calculate_damage(self, skill, attacker, defender):
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

    def _reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
