from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.opponent.display_name}: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        turn_queue = []
        while True:
            turn_queue.clear()
            self.player_choice_phase(self.player, turn_queue)
            self.player_choice_phase(self.opponent, turn_queue)
            self.resolution_phase(turn_queue)
            
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player, turn_queue):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                skill = self.choose_skill(current_player)
                if skill:
                    turn_queue.append((current_player, "attack", skill))
                    break
            elif swap_button == choice:
                new_creature = self.choose_creature(current_player)
                if new_creature:
                    turn_queue.append((current_player, "swap", new_creature))
                    break

    def choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def choose_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def resolution_phase(self, turn_queue):
        turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed, random.random()))
        
        for player, action, target in turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                self.execute_skill(player, target)

    def execute_skill(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {final_damage} damage!")

    def get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, creature_type), 1)

    def check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                return True
            
            if player.active_creature.hp == 0:
                new_creature = self.force_swap(player)
                if new_creature:
                    player.active_creature = new_creature
                else:
                    winner = self.opponent if player == self.player else self.player
                    self._show_text(self.player, f"{winner.display_name} wins the battle!")
                    return True
        return False

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return None
        choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
