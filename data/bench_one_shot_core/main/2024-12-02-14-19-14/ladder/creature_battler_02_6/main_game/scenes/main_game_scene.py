from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
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
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot Choice Phase
            self.bot_chosen_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution Phase
            self._resolve_turn()
            
            # Check for battle end
            if self.player_creature.hp <= 0 or self.bot_creature.hp <= 0:
                self._handle_battle_end()
                break

    def _get_skill_choice(self, actor, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(actor, choices).thing

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

    def _execute_skill(self, attacker, skill):
        if attacker == self.player:
            atk_creature = self.player_creature
            def_creature = self.bot_creature
        else:
            atk_creature = self.bot_creature
            def_creature = self.player_creature

        damage = atk_creature.attack + skill.base_damage - def_creature.defense
        damage = max(0, damage)  # Prevent negative damage
        def_creature.hp -= damage

        self._show_text(self.player, f"{atk_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {damage} damage!")

    def _handle_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
        
        self._transition_to_scene("MainMenuScene")
