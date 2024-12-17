from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_choice = None
        self.bot_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            self.player_choice = self.player_creature.skills[0]  # Default to first skill
            
            choice = self._wait_for_choice(self.player, choices)
            for skill in self.player_creature.skills:
                if skill.display_name == choice.display_name:
                    self.player_choice = skill
                    break

            # Bot Choice Phase
            self.bot_choice = self._wait_for_choice(self.bot, 
                [Button(skill.display_name) for skill in self.bot_creature.skills])
            for skill in self.bot_creature.skills:
                if skill.display_name == self.bot_choice.display_name:
                    self.bot_choice = skill
                    break

            # Resolution Phase
            first, second = self.determine_order()
            self.execute_turn(first)
            
            if self.check_battle_end():
                break
                
            self.execute_turn(second)
            
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_choice), (self.bot, self.bot_choice)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_choice), (self.player, self.player_choice)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_choice), (self.bot, self.bot_choice)
            return (self.bot, self.bot_choice), (self.player, self.player_choice)

    def execute_turn(self, turn):
        attacker, skill = turn
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.bot_creature
        else:
            attacker_creature = self.bot_creature
            defender_creature = self.player_creature

        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(0, damage)  # Ensure damage isn't negative
        defender_creature.hp -= damage

        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
