from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            choices = [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills]
            self.player_chosen_skill = self.player_creature.skills[
                choices.index(self._wait_for_choice(self.player, choices))
            ]

            # Bot choice phase
            self.bot_chosen_skill = self._wait_for_choice(
                self.bot, 
                [DictionaryChoice(skill.display_name) for skill in self.bot_creature.skills]
            )
            self.bot_chosen_skill = self.bot_creature.skills[0]  # Bot always uses first skill

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(first)
            if self.check_battle_end():
                break
                
            self.execute_move(second)
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_chosen_skill), (self.bot, self.bot_chosen_skill)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_chosen_skill), (self.player, self.player_chosen_skill)
        else:
            actors = [(self.player, self.player_chosen_skill), (self.bot, self.bot_chosen_skill)]
            random.shuffle(actors)
            return actors[0], actors[1]

    def execute_move(self, actor_and_skill):
        actor, skill = actor_and_skill
        attacker = self.player_creature if actor == self.player else self.bot_creature
        defender = self.bot_creature if actor == self.player else self.player_creature
        
        damage = skill.base_damage + attacker.attack - defender.defense
        damage = max(0, damage)  # Ensure damage isn't negative
        
        defender.hp -= damage
        defender.hp = max(0, defender.hp)  # Ensure HP doesn't go negative
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

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
