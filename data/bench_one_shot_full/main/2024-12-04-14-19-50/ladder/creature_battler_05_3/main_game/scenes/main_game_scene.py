from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
{"> Swap" if self.get_available_creatures(self.player) else ""}
"""

    def calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5
            
        return int(raw_damage * multiplier)

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_fainted(self, player):
        if player.active_creature.hp <= 0:
            available = self.get_available_creatures(player)
            if not available:
                return False
                
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def run(self):
        while True:
            # Build choice list based on available options
            choices = [Button("Attack")]
            available_creatures = self.get_available_creatures(self.player)
            if available_creatures:
                choices.append(Button("Swap"))
            
            choice = self._wait_for_choice(self.player, choices)
            
            player_action = None
            if choice.display_name == "Attack":
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                player_action = ("attack", skill_choice.thing)
            else:
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                player_action = ("swap", creature_choice.thing)

            # Bot turn
            bot_action = ("attack", self.bot.active_creature.skills[0])  # Simple bot just uses first skill

            # Resolve actions
            if player_action[0] == "swap":
                self.player.active_creature = player_action[1]
            if bot_action[0] == "swap":
                self.bot.active_creature = bot_action[1]

            # Execute attacks
            if player_action[0] == "attack" and bot_action[0] == "attack":
                if self.player.active_creature.speed >= self.bot.active_creature.speed:
                    first, second = (self.player, player_action), (self.bot, bot_action)
                else:
                    first, second = (self.bot, bot_action), (self.player, player_action)
                    
                for attacker, action in [first, second]:
                    if attacker == self.player:
                        defender = self.bot
                    else:
                        defender = self.player
                        
                    damage = self.calculate_damage(
                        action[1], 
                        attacker.active_creature,
                        defender.active_creature
                    )
                    defender.active_creature.hp -= damage
                    
                    self._show_text(self.player, 
                        f"{attacker.active_creature.display_name} used {action[1].display_name}! "
                        f"Dealt {damage} damage!")
                    
                    if not self.handle_fainted(defender):
                        self._show_text(self.player, 
                            f"{'You' if defender == self.bot else 'The opponent'} have no more creatures!")
                        self._transition_to_scene("MainMenuScene")
                        return
