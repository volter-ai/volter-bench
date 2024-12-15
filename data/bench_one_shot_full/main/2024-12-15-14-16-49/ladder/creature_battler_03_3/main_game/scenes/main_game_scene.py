from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_chosen_skill = None
        self.bot_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            skill_buttons = [Button(skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, skill_buttons)
            self.player_chosen_skill = self.player_creature.skills[skill_buttons.index(choice)]

            # Bot choice phase
            bot_choice = self._wait_for_choice(self.bot, [Button(skill.display_name) for skill in self.bot_creature.skills])
            self.bot_chosen_skill = self.bot_creature.skills[0]  # Bot always uses first skill for simplicity

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute skills
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

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def execute_turn(self, attacker):
        if attacker == self.player:
            skill = self.player_chosen_skill
            atk_creature = self.player_creature
            def_creature = self.bot_creature
        else:
            skill = self.bot_chosen_skill
            atk_creature = self.bot_creature
            def_creature = self.player_creature

        # Calculate damage
        raw_damage = atk_creature.attack + skill.base_damage - def_creature.defense
        multiplier = self.get_type_multiplier(skill.skill_type, def_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        def_creature.hp = max(0, def_creature.hp - final_damage)
        
        # Show result
        self._show_text(self.player, f"{atk_creature.display_name} used {skill.display_name}!")
        if multiplier > 1:
            self._show_text(self.player, "It's super effective!")
        elif multiplier < 1:
            self._show_text(self.player, "It's not very effective...")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            self._quit_whole_game()
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"{self.bot_creature.display_name} fainted! You win!")
            self._quit_whole_game()
            return True
        return False
