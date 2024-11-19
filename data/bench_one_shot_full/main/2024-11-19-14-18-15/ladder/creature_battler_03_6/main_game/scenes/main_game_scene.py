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
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot choice phase
            self.bot_chosen_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution phase
            first, second = self._determine_turn_order()
            
            # Execute moves
            self._execute_turn(first)
            if self._check_battle_end():
                break
                
            self._execute_turn(second)
            if self._check_battle_end():
                break

    def _get_skill_choice(self, actor, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(actor, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_turn_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_chosen_skill), (self.bot, self.bot_chosen_skill)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_chosen_skill), (self.player, self.player_chosen_skill)
        else:
            actors = [(self.player, self.player_chosen_skill), (self.bot, self.bot_chosen_skill)]
            random.shuffle(actors)
            return actors[0], actors[1]

    def _calculate_damage(self, attacker, skill, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf":
                multiplier = 2.0
            elif defender.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire":
                multiplier = 2.0
            elif defender.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water":
                multiplier = 2.0
            elif defender.creature_type == "fire":
                multiplier = 0.5
                
        return int(raw_damage * multiplier)

    def _execute_turn(self, turn):
        actor, skill = turn
        attacker = self.player_creature if actor == self.player else self.bot_creature
        defender = self.bot_creature if actor == self.player else self.player_creature
        
        damage = self._calculate_damage(attacker, skill, defender)
        defender.hp = max(0, defender.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} was defeated!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"You defeated the opponent's {self.bot_creature.display_name}!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
