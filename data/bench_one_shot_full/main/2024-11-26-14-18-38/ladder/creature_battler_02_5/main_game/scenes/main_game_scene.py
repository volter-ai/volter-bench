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
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

VS

{self.bot.display_name}'s {self.bot_creature.display_name}:
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Attack: {self.bot_creature.attack}
Defense: {self.bot_creature.defense}
Speed: {self.bot_creature.speed}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot choice phase
            self.bot_chosen_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution phase
            self._resolve_turn()
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
        
        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self):
        first, second = self._determine_turn_order()
        
        # Execute first attack
        damage = self._calculate_damage(first[0], first[1], first[2], first[3])
        first[3].hp -= damage
        self._show_text(self.player, f"{first[0].display_name} used {first[1].display_name} for {damage} damage!")
        
        # Execute second attack if target still alive
        if first[3].hp > 0:
            damage = self._calculate_damage(second[0], second[1], second[2], second[3])
            second[3].hp -= damage
            self._show_text(self.player, f"{second[0].display_name} used {second[1].display_name} for {damage} damage!")

    def _determine_turn_order(self):
        player_data = (self.player_creature, self.player_chosen_skill, self.bot_creature, self.bot_creature)
        bot_data = (self.bot_creature, self.bot_chosen_skill, self.player_creature, self.player_creature)
        
        if self.player_creature.speed > self.bot_creature.speed:
            return player_data, bot_data
        elif self.bot_creature.speed > self.player_creature.speed:
            return bot_data, player_data
        else:
            return (player_data, bot_data) if random.random() < 0.5 else (bot_data, player_data)

    def _calculate_damage(self, attacker, skill, defender, target):
        return max(0, attacker.attack + skill.base_damage - defender.defense)
