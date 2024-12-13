from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creatures to max HP
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._handle_player_turn()
            
            # Bot Choice Phase
            bot_skill = self._handle_bot_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, bot_skill)
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost the battle!")
                self._quit_whole_game()
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won the battle!")
                self._quit_whole_game()

    def _handle_player_turn(self) -> Skill:
        self._show_text(self.player, "Choose your skill!")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        return self._wait_for_choice(self.player, choices).thing

    def _handle_bot_turn(self) -> Skill:
        self._show_text(self.bot, "Bot choosing skill...")
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        return self._wait_for_choice(self.bot, choices).thing

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _resolve_turn(self, player_skill: Skill, bot_skill: Skill):
        # Determine order
        if self.player_creature.speed > self.bot_creature.speed:
            first = (self.player_creature, self.bot_creature, player_skill)
            second = (self.bot_creature, self.player_creature, bot_skill)
        elif self.player_creature.speed < self.bot_creature.speed:
            first = (self.bot_creature, self.player_creature, bot_skill)
            second = (self.player_creature, self.bot_creature, player_skill)
        else:
            import random
            if random.random() < 0.5:
                first = (self.player_creature, self.bot_creature, player_skill)
                second = (self.bot_creature, self.player_creature, bot_skill)
            else:
                first = (self.bot_creature, self.player_creature, bot_skill)
                second = (self.player_creature, self.bot_creature, player_skill)

        # Execute skills in order
        for attacker, defender, skill in [first, second]:
            if defender.hp > 0:  # Only attack if defender still alive
                damage = self._calculate_damage(attacker, defender, skill)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
