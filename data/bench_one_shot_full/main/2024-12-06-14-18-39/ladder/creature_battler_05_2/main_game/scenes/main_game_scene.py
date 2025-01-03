from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature

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
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            self.check_battle_end()

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skills = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                
                if skill_choice != back_button:
                    return {"type": "attack", "skill": skill_choice.thing}
                    
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                if available_creatures:
                    back_button = Button("Back")
                    swap_choice = self._wait_for_choice(player, available_creatures + [back_button])
                    
                    if swap_choice != back_button:
                        return {"type": "swap", "creature": swap_choice.thing}

    def resolve_turn(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]
            
        # Then handle attacks
        actions = [(self.player, p_action), (self.bot, b_action)]
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for player, action in actions:
            if action["type"] == "attack":
                target = self.bot if player == self.player else self.player
                self.execute_attack(player, target, action["skill"])
                
                if self.force_swap_if_needed(target):
                    self.check_battle_end()

    def execute_attack(self, attacker, defender, skill):
        a_creature = attacker.active_creature
        d_creature = defender.active_creature
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = skill.base_damage + a_creature.attack - d_creature.defense
        else:
            raw_damage = (skill.base_damage * a_creature.sp_attack) / d_creature.sp_defense
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, d_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        d_creature.hp = max(0, d_creature.hp - final_damage)
        
        self._show_text(attacker, f"{a_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{d_creature.display_name} took {final_damage} damage!")

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def force_swap_if_needed(self, player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                choices = [SelectThing(c) for c in available_creatures]
                self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
                choice = self._wait_for_choice(player, choices)
                player.active_creature = choice.thing
                return False
            return True
        return False

    def check_battle_end(self):
        p_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        b_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
        elif not b_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
