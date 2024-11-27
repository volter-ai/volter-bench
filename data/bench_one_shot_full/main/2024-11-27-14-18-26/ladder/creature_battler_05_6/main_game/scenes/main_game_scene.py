from typing import Dict, Optional
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature, Skill

TYPE_EFFECTIVENESS = {
    "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
    "fire": {"normal": 1, "fire": 1, "water": 0.5, "leaf": 2},
    "water": {"normal": 1, "fire": 2, "water": 1, "leaf": 0.5},
    "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 1}
}

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                if self.check_battle_end():
                    self._quit_whole_game()
                    return
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                if self.check_battle_end():
                    self._quit_whole_game()
                    return
                continue
                
            # Resolution phase
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()
                return

    def get_player_action(self, current_player: Player) -> Optional[Dict]:
        if self.needs_forced_swap(current_player):
            return self.handle_forced_swap(current_player)
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(current_player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.handle_attack_choice(current_player)
        else:
            return self.handle_swap_choice(current_player)

    def handle_attack_choice(self, current_player: Player) -> Dict:
        skill_choices = [
            SelectThing(skill) 
            for skill in current_player.active_creature.skills
        ]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(current_player, skill_choices + [back_button])
        
        if choice == back_button:
            return self.get_player_action(current_player)
            
        return {"type": "attack", "skill": choice.thing}

    def handle_swap_choice(self, current_player: Player) -> Dict:
        available_creatures = [
            SelectThing(creature)
            for creature in current_player.creatures
            if creature != current_player.active_creature and creature.hp > 0
        ]
        
        if not available_creatures:
            self._show_text(current_player, "No creatures available to swap!")
            return self.get_player_action(current_player)
            
        back_button = Button("Back")
        choice = self._wait_for_choice(current_player, available_creatures + [back_button])
        
        if choice == back_button:
            return self.get_player_action(current_player)
            
        return {"type": "swap", "creature": choice.thing}

    def needs_forced_swap(self, current_player: Player) -> bool:
        return current_player.active_creature.hp <= 0

    def handle_forced_swap(self, current_player: Player) -> Optional[Dict]:
        available_creatures = [
            SelectThing(creature)
            for creature in current_player.creatures
            if creature.hp > 0
        ]
        
        if not available_creatures:
            return None
            
        choice = self._wait_for_choice(current_player, available_creatures)
        return {"type": "swap", "creature": choice.thing}

    def resolve_actions(self, player_action: Dict, bot_action: Dict):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            
        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                self.resolve_attack(self.player, self.bot, player_action["skill"])
                if self.bot.active_creature.hp > 0:
                    self.resolve_attack(self.bot, self.player, bot_action["skill"])
            else:
                self.resolve_attack(self.bot, self.player, bot_action["skill"])
                if self.player.active_creature.hp > 0:
                    self.resolve_attack(self.player, self.bot, player_action["skill"])

    def resolve_attack(self, attacker: Player, defender: Player, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (
                attacker.active_creature.attack + 
                skill.base_damage - 
                defender.active_creature.defense
            )
        else:
            raw_damage = (
                skill.base_damage * 
                attacker.active_creature.sp_attack / 
                defender.active_creature.sp_defense
            )
            
        # Apply type effectiveness
        effectiveness = TYPE_EFFECTIVENESS[skill.skill_type][defender.active_creature.creature_type]
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        self._show_text(
            attacker,
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!"
        )

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
