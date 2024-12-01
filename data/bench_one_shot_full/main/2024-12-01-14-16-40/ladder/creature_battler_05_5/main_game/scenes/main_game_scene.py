from typing import List, Tuple
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
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

Your turn options:
> Attack (Use a skill)
> Swap (Change creature)
"""

    def run(self):
        # Initialize battle
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.bot.display_name}")
        
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions in speed order
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, current_player: Player) -> DictionaryChoice:
        # First level menu
        attack_choice = Button("Attack")
        swap_choice = Button("Swap")
        choice = self._wait_for_choice(current_player, [attack_choice, swap_choice])
        
        if choice == attack_choice:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
            skill_choice = self._wait_for_choice(current_player, skill_choices)
            
            action = DictionaryChoice("Use " + skill_choice.thing.display_name)
            action.value = {
                "type": "attack",
                "skill_id": skill_choice.thing.prototype_id
            }
            return action
            
        else:
            # Show available creatures
            available_creatures = [c for c in current_player.creatures if c.hp > 0 and c != current_player.active_creature]
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choice = self._wait_for_choice(current_player, creature_choices)
            
            action = DictionaryChoice("Switch to " + creature_choice.thing.display_name)
            action.value = {
                "type": "swap",
                "creature_id": creature_choice.thing.prototype_id
            }
            return action

    def resolve_turn(self, player_action: DictionaryChoice, bot_action: DictionaryChoice):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Handle swaps first
        for player, action in actions:
            if action.value["type"] == "swap":
                # Find creature by ID
                new_creature = next(c for c in player.creatures if c.prototype_id == action.value["creature_id"])
                player.active_creature = new_creature
                self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
        
        # Then handle attacks in speed order
        actions = [(p, a) for p, a in actions if a.value["type"] == "attack"]
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for attacker, action in actions:
            if attacker.active_creature.hp <= 0:
                continue
                
            defender = self.bot if attacker == self.player else self.player
            # Find skill by ID
            skill = next(s for s in attacker.active_creature.skills if s.prototype_id == action.value["skill_id"])
            
            # Calculate damage
            if skill.is_physical:
                raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
            else:
                raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
                
            # Apply type effectiveness
            multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
            final_damage = int(raw_damage * multiplier)
            
            # Apply damage
            defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
            self._show_text(self.player, 
                f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! "
                f"Dealt {final_damage} damage!")
            
            # Force swap if creature fainted
            if defender.active_creature.hp <= 0:
                self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
                self.force_swap(defender)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type or skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
            self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = creature_choice.thing
            self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")

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
