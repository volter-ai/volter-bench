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
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

{self.bot.display_name}'s {self.bot_creature.display_name}:
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Type: {self.bot_creature.creature_type}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot Choice Phase
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution Phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )
            
            # Execute skills
            for attacker, attacker_creature, skill in [first, second]:
                if attacker == self.player:
                    defender = self.bot
                    defender_creature = self.bot_creature
                else:
                    defender = self.player
                    defender_creature = self.player_creature
                    
                damage = self._calculate_damage(skill, attacker_creature, defender_creature)
                defender_creature.hp -= damage
                
                self._show_text(self.player, 
                    f"{attacker_creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage to {defender_creature.display_name}!")
                
                if defender_creature.hp <= 0:
                    defender_creature.hp = 0
                    winner = attacker
                    self._show_text(self.player, 
                        f"{defender_creature.display_name} fainted! "
                        f"{winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills 
                   if skill.display_name == choice.display_name)

    def _determine_order(self, p1_data, p2_data):
        p1_speed = p1_data[1].speed
        p2_speed = p2_data[1].speed
        
        if p1_speed > p2_speed:
            return p1_data, p2_data
        elif p2_speed > p1_speed:
            return p2_data, p1_data
        else:
            return random.sample([p1_data, p2_data], 2)

    def _calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * effectiveness)
        return max(0, final_damage)

    def _get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)
