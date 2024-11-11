from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature stats
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
            else:
                available_creatures = [
                    SelectThing(creature) 
                    for creature in player.creatures 
                    if creature != player.active_creature and creature.hp > 0
                ]
                back_button = Button("Back")
                swap_choice = self._wait_for_choice(player, available_creatures + [back_button])
                if swap_choice != back_button:
                    return ("swap", swap_choice.thing)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type multiplier
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

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Sort by speed for attacks
        actions.sort(key=lambda x: (
            x[1][0] != "swap",  # Swaps go first
            -x[0].active_creature.speed  # Then sort by speed
        ))

        for actor, action in actions:
            if action[0] == "swap":
                actor.active_creature = action[1]
                self._show_text(actor, f"{actor.display_name} swapped to {action[1].display_name}!")
            else:
                target = self.bot if actor == self.player else self.player
                damage = self.calculate_damage(actor.active_creature, target.active_creature, action[1])
                target.active_creature.hp = max(0, target.active_creature.hp - damage)
                self._show_text(actor, f"{actor.active_creature.display_name} used {action[1].display_name}!")
                self._show_text(actor, f"It dealt {damage} damage!")
                
                # Only check for knockouts after damage is dealt
                if target.active_creature.hp <= 0:
                    self.handle_knockout(target)

    def handle_knockout(self, player: Player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            swap_choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, swap_choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {choice.thing.display_name}!")

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)

        if not player_has_creatures or not bot_has_creatures:
            winner = self.player if player_has_creatures else self.bot
            self._show_text(self.player, f"{winner.display_name} wins the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
