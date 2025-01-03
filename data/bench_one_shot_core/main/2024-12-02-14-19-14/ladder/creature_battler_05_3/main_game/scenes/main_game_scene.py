import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Main battle loop
            if not self.can_battle(self.player) or not self.can_battle(self.bot):
                self.end_battle()
                return

            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)

    def can_battle(self, player: Player) -> bool:
        return any(c.hp > 0 for c in player.creatures)

    def get_player_action(self, player: Player):
        while True:
            attack = Button("Attack")
            swap = Button("Swap")
            choice = self._wait_for_choice(player, [attack, swap])

            if choice == attack:
                skills = [SelectThing(s) for s in player.active_creature.skills]
                back = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back])
                if skill_choice != back:
                    return ("attack", skill_choice.thing)
            
            elif choice == swap:
                available = [c for c in player.creatures 
                           if c.hp > 0 and c != player.active_creature]
                if not available:
                    self._show_text(player, "No creatures available to swap!")
                    continue
                    
                creatures = [SelectThing(c) for c in available]
                back = Button("Back")
                creature_choice = self._wait_for_choice(player, creatures + [back])
                if creature_choice != back:
                    return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first)
        self.execute_action(second)

        # Check for knockouts
        self.handle_knockouts()

    def get_action_order(self, player_action, bot_action):
        p_speed = self.player.active_creature.speed
        b_speed = self.bot.active_creature.speed
        
        if p_speed > b_speed or (p_speed == b_speed and random.random() < 0.5):
            return (player_action, self.player, self.bot), (bot_action, self.bot, self.player)
        return (bot_action, self.bot, self.player), (player_action, self.player, self.bot)

    def execute_action(self, action_tuple):
        action, attacker, defender = action_tuple
        if action[0] == "attack":
            skill = action[1]
            damage = self.calculate_damage(skill, attacker.active_creature, defender.active_creature)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} for {damage} damage!")

    def calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockouts(self):
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                available = [c for c in player.creatures if c.hp > 0]
                if available:
                    self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
                    creatures = [SelectThing(c) for c in available]
                    choice = self._wait_for_choice(player, creatures)
                    player.active_creature = choice.thing

    def end_battle(self):
        player_lost = not self.can_battle(self.player)
        self._show_text(self.player, "You lost!" if player_lost else "You won!")
        
        # Reset all creatures' HP before leaving the scene
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
                
        self._transition_to_scene("MainMenuScene")
