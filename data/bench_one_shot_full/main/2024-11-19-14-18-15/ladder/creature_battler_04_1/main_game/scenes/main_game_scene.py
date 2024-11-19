from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A battle begins between {self.player.display_name} and {self.bot.display_name}!")
        
        while True:
            # Player choice phase
            self.player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot choice phase
            self.bot_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution phase
            self._resolve_turn()
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost the battle!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won the battle!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self):
        # Determine order
        first, second = self._determine_order()
        
        # Execute skills
        self._execute_skill(first[0], first[1], first[2], second[2])
        if second[2].hp > 0:  # Only execute second skill if target still alive
            self._execute_skill(second[0], second[1], second[2], first[2])

    def _determine_order(self):
        player_speed = self.player_creature.speed
        bot_speed = self.bot_creature.speed
        
        if player_speed > bot_speed:
            return (self.player, self.player_skill, self.player_creature, self.bot_creature), \
                   (self.bot, self.bot_skill, self.bot_creature, self.player_creature)
        elif bot_speed > player_speed:
            return (self.bot, self.bot_skill, self.bot_creature, self.player_creature), \
                   (self.player, self.player_skill, self.player_creature, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_skill, self.player_creature, self.bot_creature), \
                       (self.bot, self.bot_skill, self.bot_creature, self.player_creature)
            else:
                return (self.bot, self.bot_skill, self.bot_creature, self.player_creature), \
                       (self.player, self.player_skill, self.player_creature, self.bot_creature)

    def _execute_skill(self, user, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * factor)
        
        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)
        
        # Show result
        effectiveness = "It's super effective!" if factor > 1 else "It's not very effective..." if factor < 1 else ""
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {effectiveness}")

    def _get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
