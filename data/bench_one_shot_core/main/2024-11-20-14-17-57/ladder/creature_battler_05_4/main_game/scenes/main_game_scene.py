from typing import List, Optional
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        
    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

What will you do?
> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_player_turn(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self._handle_player_turn(self.bot)
            if not bot_action:
                continue
                
            # Resolve actions
            self._resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                # Reset all creatures' HP before leaving scene
                for creature in self.player.creatures:
                    creature.hp = creature.max_hp
                for creature in self.bot.creatures:
                    creature.hp = creature.max_hp
                self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, current_player: Player) -> Optional[DictionaryChoice]:
        while True:
            choices = [
                Button("Attack"),
                Button("Swap")
            ]
            
            choice = self._wait_for_choice(current_player, choices)
            
            if choice.display_name == "Attack":
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                
                if isinstance(skill_choice, Button):
                    continue
                    
                action = DictionaryChoice("action")
                action.value = {"type": "attack", "skill": skill_choice.thing}
                return action
                
            elif choice.display_name == "Swap":
                available_creatures = [
                    creature for creature in current_player.creatures 
                    if creature != current_player.active_creature and creature.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(current_player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(current_player, creature_choices)
                
                if isinstance(creature_choice, Button):
                    continue
                    
                action = DictionaryChoice("action")
                action.value = {"type": "swap", "creature": creature_choice.thing}
                return action

    def _resolve_turn(self, player_action: DictionaryChoice, bot_action: DictionaryChoice):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Handle swaps first
        for player, action in actions:
            if action.value["type"] == "swap":
                player.active_creature = action.value["creature"]
                self._show_text(player, f"{player.display_name} swapped to {action.value['creature'].display_name}!")
        
        # Then handle attacks in speed order
        attack_actions = [(p, a) for p, a in actions if a.value["type"] == "attack"]
        attack_actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for attacker, action in attack_actions:
            if attacker == self.player:
                defender = self.bot
            else:
                defender = self.player
                
            self._resolve_attack(attacker, defender, action.value["skill"])

    def _resolve_attack(self, attacker: Player, defender: Player, skill: Skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        effectiveness_text = ""
        if effectiveness > 1:
            effectiveness_text = "It's super effective!"
        elif effectiveness < 1:
            effectiveness_text = "It's not very effective..."
            
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness_text}")

    def _get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self) -> bool:
        def has_available_creatures(player: Player) -> bool:
            return any(creature.hp > 0 for creature in player.creatures)
            
        if not has_available_creatures(self.player):
            self._show_text(self.player, "You lost the battle!")
            return True
            
        if not has_available_creatures(self.bot):
            self._show_text(self.player, "You won the battle!")
            return True
            
        if self.player.active_creature.hp <= 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            if available:
                choices = [SelectThing(creature) for creature in available]
                choice = self._wait_for_choice(self.player, choices)
                self.player.active_creature = choice.thing
                return False
                
        if self.bot.active_creature.hp <= 0:
            available = [c for c in self.bot.creatures if c.hp > 0]
            if available:
                self.bot.active_creature = available[0]
                return False
                
        return False
