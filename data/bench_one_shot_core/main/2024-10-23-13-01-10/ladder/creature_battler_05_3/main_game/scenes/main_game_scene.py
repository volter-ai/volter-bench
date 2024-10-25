from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from mini_game_engine.engine.lib import BotListener


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name if player_creature else 'No active creature'}: HP {player_creature.hp}/{player_creature.max_hp if player_creature else 0}
{self.opponent.display_name}'s {opponent_creature.display_name if opponent_creature else 'No active creature'}: HP {opponent_creature.hp}/{opponent_creature.max_hp if opponent_creature else 0}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.player_turn(self.player)
            self.player_turn(self.opponent)
            self._resolve_turn()
            if self._check_battle_end():
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def _initialize_battle(self):
        if not self.player.active_creature and self.player.creatures:
            self.player.active_creature = self.player.creatures[0]
        if not self.opponent.active_creature and self.opponent.creatures:
            self.opponent.active_creature = self.opponent.creatures[0]

    def player_turn(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                skill = self._choose_skill(player)
                if skill:
                    self.turn_queue.append((player, "attack", skill))
                    break
            elif choice == swap_button:
                new_creature = self._choose_creature(player)
                if new_creature:
                    self.turn_queue.append((player, "swap", new_creature))
                    break

    def _choose_skill(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        if not isinstance(player._listener, BotListener):
            choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice.thing

    def _choose_creature(self, player):
        choices = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        if not isinstance(player._listener, BotListener):
            choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice.thing if isinstance(choice, SelectThing) else None

    def _resolve_turn(self):
        self.turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed))
        for player, action, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                self._resolve_attack(player, target)
        self.turn_queue.clear()

    def _resolve_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            new_creature = self._choose_creature(defender)
            if new_creature:
                defender.active_creature = new_creature
                self._show_text(defender, f"{defender.display_name} sent out {new_creature.display_name}!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)

    def _get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        if all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self.player.active_creature = None
        self.opponent.active_creature = None
