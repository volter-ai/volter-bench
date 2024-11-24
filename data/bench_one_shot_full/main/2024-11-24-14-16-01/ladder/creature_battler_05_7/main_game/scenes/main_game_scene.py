from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p1 = self.player
        p2 = self.bot
        
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            p1_action = self.get_player_action(self.player)
            p2_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(p1_action, p2_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Properly end the game after showing the winner
                self._quit_whole_game()

    def get_player_action(self, player):
        # First check what choices are available
        choices = [Button("Attack")]
        
        # Only add swap if there are valid creatures to swap to
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if valid_creatures:
            choices.append(Button("Swap"))
            
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return ("attack", self._wait_for_choice(player, choices).thing)
        else:
            choices = [SelectThing(creature) for creature in valid_creatures]
            return ("swap", self._wait_for_choice(player, choices).thing)

    def resolve_turn(self, p1_action, p2_action):
        actions = [p1_action, p2_action]
        players = [self.player, self.bot]
        
        # Swaps go first
        for i, action in enumerate(actions):
            if action[0] == "swap":
                players[i].active_creature = action[1]
                self._show_text(players[i], f"{players[i].display_name} swapped to {action[1].display_name}!")

        # Then attacks in speed order
        attackers = []
        for i, action in enumerate(actions):
            if action[0] == "attack":
                attackers.append((i, players[i], action[1]))
                
        if len(attackers) == 2:
            # Sort by speed
            attackers.sort(key=lambda x: x[1].active_creature.speed, reverse=True)
            
        for i, attacker, skill in attackers:
            defender = players[1-i]
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")
            
            if defender.active_creature.hp == 0:
                self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
                valid_creatures = [c for c in defender.creatures if c.hp > 0]
                if valid_creatures:
                    choices = [SelectThing(c) for c in valid_creatures]
                    new_creature = self._wait_for_choice(defender, choices).thing
                    defender.active_creature = new_creature
                    self._show_text(defender, f"{defender.display_name} sent out {new_creature.display_name}!")

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if not any(c.hp > 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
