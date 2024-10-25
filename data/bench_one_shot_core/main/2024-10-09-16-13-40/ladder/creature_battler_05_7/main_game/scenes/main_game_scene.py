from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        self.player_action = None
        self.bot_action = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.bot.display_name}: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            self.player_choice_phase(self.player)
            self.player_choice_phase(self.bot)
            self.resolution_phase()
            
            if self.check_battle_end():
                break

        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                skill = self.choose_skill(current_player)
                if skill:
                    if current_player == self.player:
                        self.player_action = ("attack", skill)
                    else:
                        self.bot_action = ("attack", skill)
                    break
            elif swap_button == choice:
                new_creature = self.choose_creature(current_player)
                if new_creature:
                    if current_player == self.player:
                        self.player_action = ("swap", new_creature)
                    else:
                        self.bot_action = ("swap", new_creature)
                    break

    def choose_skill(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def choose_creature(self, player):
        choices = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def resolution_phase(self):
        players = [self.player, self.bot]
        actions = [self.player_action, self.bot_action]

        # First, handle all swaps
        for i, (player, action) in enumerate(zip(players, actions)):
            if action[0] == "swap":
                opponent = players[1-i]
                opponent_action = actions[1-i]
                self.execute_swap(player, action[1])
                if opponent_action[0] == "attack":
                    self.execute_attack(opponent, player, opponent_action[1])
                    actions[1-i] = None  # Mark this attack as resolved

        # Then, handle remaining attacks
        for i, (player, action) in enumerate(zip(players, actions)):
            if action and action[0] == "attack":
                opponent = players[1-i]
                self.execute_attack(player, opponent, action[1])

        self.player_action = None
        self.bot_action = None

    def execute_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def execute_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")
        if defender.active_creature.hp == 0:
            self.force_swap(defender)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            new_creature = self.choose_creature(player)
            if new_creature:
                player.active_creature = new_creature
                self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")
            else:
                player.active_creature = available_creatures[0]
                self._show_text(player, f"{player.display_name} was forced to use {player.active_creature.display_name}!")

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures_state(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
