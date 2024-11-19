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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
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
                self._show_text(self.bot, "You won!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.bot, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, actor, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(actor, choices)
        return creature.skills[choices.index(choice)]

    def _resolve_turn(self):
        # Determine order based on speed
        if self.player_creature.speed > self.bot_creature.speed:
            first, second = self.player, self.bot
            first_skill, second_skill = self.player_chosen_skill, self.bot_chosen_skill
        elif self.bot_creature.speed > self.player_creature.speed:
            first, second = self.bot, self.player
            first_skill, second_skill = self.bot_chosen_skill, self.player_chosen_skill
        else:
            # Random order if speeds are equal
            if random.random() < 0.5:
                first, second = self.player, self.bot
                first_skill, second_skill = self.player_chosen_skill, self.bot_chosen_skill
            else:
                first, second = self.bot, self.player
                first_skill, second_skill = self.bot_chosen_skill, self.player_chosen_skill

        # Execute skills in order
        self._execute_skill(first, first_skill)
        if self.player_creature.hp > 0 and self.bot_creature.hp > 0:
            self._execute_skill(second, second_skill)

    def _execute_skill(self, actor, skill):
        attacker = self.player_creature if actor == self.player else self.bot_creature
        defender = self.bot_creature if actor == self.player else self.player_creature
        
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp = max(0, defender.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.bot, f"{attacker.display_name} used {skill.display_name}!")
