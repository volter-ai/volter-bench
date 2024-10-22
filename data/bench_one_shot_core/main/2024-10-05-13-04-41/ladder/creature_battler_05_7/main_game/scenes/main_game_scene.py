from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.foe.active_creature = self.foe.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.foe.display_name}: {self.foe.active_creature.display_name} (HP: {self.foe.active_creature.hp}/{self.foe.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            self.player_turn()
            if self.check_battle_end():
                break
            self.foe_turn()
            if self.check_battle_end():
                break
            self.resolve_turn()
        self.reset_creatures()

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill = self.choose_skill(self.player)
                if skill:
                    return ("attack", skill)
            elif choice == swap_button:
                new_creature = self.choose_creature(self.player)
                if new_creature:
                    return ("swap", new_creature)

    def foe_turn(self):
        return self.player_turn()  # For simplicity, the bot uses the same logic as the player

    def choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def choose_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def resolve_turn(self):
        player_action = self.player_turn()
        foe_action = self.foe_turn()

        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if foe_action[0] == "swap":
            self.foe.active_creature = foe_action[1]

        if player_action[0] == "attack" and foe_action[0] == "attack":
            player_speed = self.player.active_creature.speed
            foe_speed = self.foe.active_creature.speed

            if player_speed > foe_speed:
                self.execute_skill(self.player, self.foe, player_action[1])
                if not self.check_battle_end() and self.foe.active_creature.hp > 0:
                    self.execute_skill(self.foe, self.player, foe_action[1])
            elif foe_speed > player_speed:
                self.execute_skill(self.foe, self.player, foe_action[1])
                if not self.check_battle_end() and self.player.active_creature.hp > 0:
                    self.execute_skill(self.player, self.foe, player_action[1])
            else:
                # Equal speed, randomly decide who goes first
                if random.choice([True, False]):
                    self.execute_skill(self.player, self.foe, player_action[1])
                    if not self.check_battle_end() and self.foe.active_creature.hp > 0:
                        self.execute_skill(self.foe, self.player, foe_action[1])
                else:
                    self.execute_skill(self.foe, self.player, foe_action[1])
                    if not self.check_battle_end() and self.player.active_creature.hp > 0:
                        self.execute_skill(self.player, self.foe, player_action[1])

    def execute_skill(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        weakness_factor = self.get_weakness_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)

        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
            self.force_swap(defender)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
        
        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
            self._show_text(player, f"{player.active_creature.display_name} was sent out!")
        else:
            self._show_text(player, "Choose a creature to swap in:")
            new_creature = self.choose_creature(player)
            if new_creature:
                player.active_creature = new_creature
                self._show_text(player, f"{player.active_creature.display_name} was sent out!")
            else:
                player.active_creature = available_creatures[0]
                self._show_text(player, f"{player.active_creature.display_name} was sent out!")
        return True

    def get_weakness_factor(self, skill_type, creature_type):
        weakness_chart = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return weakness_chart.get((skill_type, creature_type), 1)

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        if all(creature.hp == 0 for creature in self.foe.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.foe.creatures:
            creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
