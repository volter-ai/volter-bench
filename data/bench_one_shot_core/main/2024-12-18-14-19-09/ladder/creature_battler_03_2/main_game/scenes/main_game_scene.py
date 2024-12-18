from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

VS

{self.bot.display_name}'s {self.bot_creature.display_name}
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Type: {self.bot_creature.creature_type}
"""

    def run(self):
        while True:
            self._show_text(self.player, str(self))
            
            # Player choice phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot choice phase
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )
            
            # Execute skills
            for attacker, creature, skill in [first, second]:
                if creature.hp <= 0:
                    continue
                    
                target = self.bot_creature if attacker == self.player else self.player_creature
                damage = self._calculate_damage(creature, target, skill)
                target.hp -= damage
                
                self._show_text(self.player, f"{creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"It dealt {damage} damage!")
                
                if target.hp <= 0:
                    winner = self.player if target == self.bot_creature else self.bot
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _determine_order(self, p1_data, p2_data):
        p1_player, p1_creature, p1_skill = p1_data
        p2_player, p2_creature, p2_skill = p2_data
        
        if p1_creature.speed > p2_creature.speed:
            return p1_data, p2_data
        elif p2_creature.speed > p1_creature.speed:
            return p2_data, p1_data
        else:
            return random.choice([(p1_data, p2_data), (p2_data, p1_data)])

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Get type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)
