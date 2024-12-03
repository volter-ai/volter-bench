from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature

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

Your other creatures: {[c.display_name for c in self.player.creatures if c != p_creature and c.hp > 0]}
Foe's other creatures: {[c.display_name for c in self.bot.creatures if c != b_creature and c.hp > 0]}"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_available_creatures(self, player):
        """Helper to get list of creatures available for swapping"""
        return [c for c in player.creatures if c != player.active_creature and c.hp > 0]

    def get_player_action(self, player):
        choices = [Button("Attack")]
        
        # Only add swap option if there are creatures to swap to
        available_creatures = self.get_available_creatures(player)
        if available_creatures:
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(s) for s in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:
            # Show available creatures
            creature_choices = [SelectThing(c) for c in available_creatures]
            return self._wait_for_choice(player, creature_choices)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        for action, actor in [(player_action, self.player), (bot_action, self.bot)]:
            if isinstance(action.thing, Creature):
                actor.active_creature = action.thing
                self._show_text(actor, f"Swapped to {action.thing.display_name}!")

        # Then handle attacks
        actions = [(player_action, self.player, self.bot), (bot_action, self.bot, self.player)]
        actions.sort(key=lambda x: x[1].active_creature.speed, reverse=True)
        
        for action, attacker, defender in actions:
            if isinstance(action.thing, Creature):
                continue
                
            skill = action.thing
            damage = self.calculate_damage(skill, attacker.active_creature, defender.active_creature)
            defender.active_creature.hp -= damage
            
            if defender.active_creature.hp < 0:
                defender.active_creature.hp = 0
                
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(defender, f"Took {damage} damage!")

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf":
                multiplier = 2.0
            elif defender.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire":
                multiplier = 2.0
            elif defender.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water":
                multiplier = 2.0
            elif defender.creature_type == "fire":
                multiplier = 0.5
                
        return int(raw_damage * multiplier)

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                self._transition_to_scene("MainMenuScene")
                return True
                
            if player.active_creature.hp <= 0:
                available = self.get_available_creatures(player)
                if available:
                    choices = [SelectThing(c) for c in available]
                    choice = self._wait_for_choice(player, choices)
                    player.active_creature = choice.thing
                    self._show_text(player, f"Switched to {choice.thing.display_name}!")
                else:
                    # If no creatures available, this player has lost
                    winner = self.bot if player == self.player else self.player
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return True
        return False
