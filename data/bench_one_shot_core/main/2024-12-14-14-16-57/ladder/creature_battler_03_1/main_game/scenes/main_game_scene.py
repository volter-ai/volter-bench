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
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.bot, "Battle Start!")

        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot Choice Phase
            self.bot_chosen_skill = self._get_skill_choice(self.bot, self.bot_creature)

            # Resolution Phase
            self._resolve_turn()

            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, actor, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(actor, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self):
        # Determine order
        first, second = self._determine_turn_order()
        
        # Execute skills
        self._execute_skill(first[0], first[1], first[2], second[2])
        if second[2].hp > 0:  # Only execute second skill if target still alive
            self._execute_skill(second[0], second[1], second[2], first[2])

    def _determine_turn_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_chosen_skill, self.player_creature), (self.bot, self.bot_chosen_skill, self.bot_creature)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_chosen_skill, self.bot_creature), (self.player, self.player_chosen_skill, self.player_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_chosen_skill, self.player_creature), (self.bot, self.bot_chosen_skill, self.bot_creature)
            return (self.bot, self.bot_chosen_skill, self.bot_creature), (self.player, self.player_chosen_skill, self.player_creature)

    def _execute_skill(self, attacker, skill, attacker_creature, defender_creature):
        # Calculate raw damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        # Show damage message
        message = f"{attacker_creature.display_name} used {skill.display_name} for {final_damage} damage!"
        self._show_text(attacker, message)
        self._show_text(self.bot if attacker == self.player else self.player, message)

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
