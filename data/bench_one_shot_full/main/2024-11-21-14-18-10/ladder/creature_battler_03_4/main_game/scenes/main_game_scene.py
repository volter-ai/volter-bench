from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{self._format_skills(self.player_creature)}
"""

    def _format_skills(self, creature):
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in creature.skills])

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        type_multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": type_multiplier = 2.0
            elif defender.creature_type == "water": type_multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": type_multiplier = 2.0
            elif defender.creature_type == "leaf": type_multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": type_multiplier = 2.0
            elif defender.creature_type == "fire": type_multiplier = 0.5

        return int(raw_damage * type_multiplier)

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills])
            player_skill = next(s for s in self.player_creature.skills 
                if s.display_name == player_skill.display_name)

            # Bot choice phase  
            bot_skill = self._wait_for_choice(self.bot,
                [Button(skill.display_name) for skill in self.bot_creature.skills])
            bot_skill = next(s for s in self.bot_creature.skills
                if s.display_name == bot_skill.display_name)

            # Resolution phase
            first = self.player_creature if self.player_creature.speed > self.bot_creature.speed \
                else self.bot_creature if self.bot_creature.speed > self.player_creature.speed \
                else random.choice([self.player_creature, self.bot_creature])
            
            if first == self.player_creature:
                self._resolve_turn(self.player_creature, self.bot_creature, player_skill)
                if self.bot_creature.hp <= 0:
                    self._show_text(self.player, "You won!")
                    self._quit_whole_game()
                self._resolve_turn(self.bot_creature, self.player_creature, bot_skill)
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lost!")
                    self._quit_whole_game()
            else:
                self._resolve_turn(self.bot_creature, self.player_creature, bot_skill)
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lost!")
                    self._quit_whole_game()
                self._resolve_turn(self.player_creature, self.bot_creature, player_skill)
                if self.bot_creature.hp <= 0:
                    self._show_text(self.player, "You won!")
                    self._quit_whole_game()

    def _resolve_turn(self, attacker, defender, skill):
        damage = self._calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, 
            f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
