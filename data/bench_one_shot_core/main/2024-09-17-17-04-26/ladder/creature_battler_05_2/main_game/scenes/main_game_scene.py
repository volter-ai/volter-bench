from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {self.player.active_creature.display_name}:
HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp}

{self.bot.display_name}'s {self.bot.active_creature.display_name}:
HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        while not self.battle_ended:
            self.turn_counter += 1
            player_action = self.player_turn(self.player)
            bot_action = self.player_turn(self.bot)
            self.resolve_turn(player_action, bot_action)
            self.check_battle_end()

        self._transition_to_scene("MainMenuScene")

    def player_turn(self, current_player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                return self.choose_attack(current_player)
            elif choice == swap_button:
                return self.choose_swap(current_player)

    def choose_attack(self, current_player: Player):
        choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(current_player, choices)

        if isinstance(choice, Button) and choice.display_name == "Back":
            return self.player_turn(current_player)
        return ("attack", choice.thing)

    def choose_swap(self, current_player: Player):
        choices = [SelectThing(creature) for creature in current_player.creatures if creature != current_player.active_creature and creature.hp > 0]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(current_player, choices)

        if isinstance(choice, Button) and choice.display_name == "Back":
            return self.player_turn(current_player)
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [
            (self.player, player_action),
            (self.bot, bot_action)
        ]
        
        # Sort actions by creature speed (descending order)
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        # Process swap actions first
        swap_actions = [action for action in actions if action[1][0] == "swap"]
        for current_player, action in swap_actions:
            self.perform_swap(current_player, action[1])
        
        # Process attack actions second
        attack_actions = [action for action in actions if action[1][0] == "attack"]
        for current_player, action in attack_actions:
            self.perform_attack(current_player, action[1])

    def perform_swap(self, current_player: Player, new_creature: Creature):
        current_player.active_creature = new_creature
        self._show_text(current_player, f"{current_player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker: Player, skill: Skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)

    def get_type_effectiveness(self, skill_type: str, defender_type: str):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return False

        choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        self.perform_swap(player, choice.thing)
        return True

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self.battle_ended = True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            self.battle_ended = True
