from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            # Player Choice Phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Bot Choice Phase  
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolution Phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )

            # Execute moves in order
            for attacker, creature, skill in [first, second]:
                if attacker == self.player:
                    defender_creature = self.bot_creature
                else:
                    defender_creature = self.player_creature

                damage = self.calculate_damage(creature, defender_creature, skill)
                defender_creature.hp -= damage

                self._show_text(self.player, 
                    f"{creature.display_name} used {skill.display_name}! Dealt {damage} damage!")

                if defender_creature.hp <= 0:
                    defender_creature.hp = 0
                    winner = self.player if attacker == self.player else self.bot
                    self._show_text(self.player,
                        f"{winner.display_name} wins! {defender_creature.display_name} fainted!")
                    
                    # Reset creatures before leaving - moved from Creature model to scene
                    self.player_creature.hp = self.player_creature.max_hp
                    self.bot_creature.hp = self.bot_creature.max_hp
                    self._transition_to_scene("MainMenuScene")
                    return

    def determine_order(self, p1_data, p2_data):
        p1_creature = p1_data[1]
        p2_creature = p2_data[1]
        if p1_creature.speed > p2_creature.speed:
            return p1_data, p2_data
        elif p2_creature.speed > p1_creature.speed:
            return p2_data, p1_data
        else:
            import random
            return random.choice([(p1_data, p2_data), (p2_data, p1_data)])

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_map = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0, 
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        return effectiveness_map.get((skill_type, defender_type), 1.0)
