from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
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
        battle_ended = False
        while not battle_ended:
            self.player_turn()
            battle_ended = self.check_battle_end()
            if battle_ended:
                break
            self.opponent_turn()
            battle_ended = self.check_battle_end()

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        action = self.get_player_action(self.player)
        if action:
            self.execute_action(self.player, self.opponent, action)
        else:
            self._show_text(self.player, f"{self.player.display_name} has no valid actions!")

    def opponent_turn(self):
        self._show_text(self.player, f"It's {self.opponent.display_name}'s turn!")
        action = self.get_player_action(self.opponent)
        if action:
            self.execute_action(self.opponent, self.player, action)
        else:
            self._show_text(self.player, f"{self.opponent.display_name} has no valid actions!")

    def get_player_action(self, acting_player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(acting_player, choices)

        if choice == attack_button:
            return self.get_attack_action(acting_player)
        elif choice == swap_button:
            return self.get_swap_action(acting_player)

    def get_attack_action(self, acting_player):
        skill_choices = [SelectThing(skill) for skill in acting_player.active_creature.skills]
        return self._wait_for_choice(acting_player, skill_choices)

    def get_swap_action(self, acting_player):
        available_creatures = [creature for creature in acting_player.creatures if creature != acting_player.active_creature and creature.hp > 0]
        if not available_creatures:
            return None
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        return self._wait_for_choice(acting_player, creature_choices)

    def execute_action(self, acting_player, defending_player, action):
        if isinstance(action.thing, Skill):
            self.execute_attack(acting_player, defending_player, action.thing)
        elif isinstance(action.thing, Creature):
            self.execute_swap(acting_player, action.thing)

    def execute_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")

    def execute_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, f"All your creatures have fainted. {self.opponent.display_name} wins!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, f"All opponent's creatures have fainted. You win!")
            return True
        elif self.player.active_creature.hp == 0:
            self.force_swap(self.player)
        elif self.opponent.active_creature.hp == 0:
            self.force_swap(self.opponent)
        return False

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            new_creature = self._wait_for_choice(player, creature_choices).thing
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} was forced to swap to {new_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures available!")

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
