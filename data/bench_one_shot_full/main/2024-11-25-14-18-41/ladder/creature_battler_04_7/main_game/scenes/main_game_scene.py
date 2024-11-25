from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.phase = "player_choice"
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = {}  # Will use player.uid as key

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Phase: {self.phase}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            if self.phase == "player_choice":
                self.handle_player_choice()
            elif self.phase == "bot_choice":
                self.handle_bot_choice()
            else:  # resolution phase
                self.resolve_turn()
                
                if self.check_battle_end():
                    self._quit_whole_game()  # Properly end the game
                    
                self.phase = "player_choice"

    def handle_player_choice(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.queued_skills[self.player.uid] = choice.thing
        self.phase = "bot_choice"

    def handle_bot_choice(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        self.queued_skills[self.bot.uid] = choice.thing
        self.phase = "resolution"

    def resolve_turn(self):
        first, second = self.determine_order()
        
        self.execute_skill(first, self.get_creature(first), self.get_creature(second), self.queued_skills[first.uid])
        if self.get_creature(second).hp > 0:
            self.execute_skill(second, self.get_creature(second), self.get_creature(first), self.queued_skills[second.uid])

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return self.player, self.bot
        elif self.bot_creature.speed > self.player_creature.speed:
            return self.bot, self.player
        else:
            return random.sample([self.player, self.bot], 2)

    def get_creature(self, player):
        return self.player_creature if player == self.player else self.bot_creature

    def execute_skill(self, attacker, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * factor)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name}! Dealt {final_damage} damage!")

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self.player_creature.hp = self.player_creature.max_hp
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self.player_creature.hp = self.player_creature.max_hp
            return True
        return False
