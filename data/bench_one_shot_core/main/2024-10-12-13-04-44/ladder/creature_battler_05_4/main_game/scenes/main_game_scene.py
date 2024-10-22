from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_queue = []
        self.battle_ended = False

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        while not self.battle_ended:
            self.player_turn()
            self.opponent_turn()
            self.resolve_turn()
            if self.check_battle_end():
                self.battle_ended = True
        
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill = self.choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("skill", self.player, skill))
                    break
            elif choice == swap_button:
                new_creature = self.choose_creature(self.player)
                if new_creature:
                    self.turn_queue.append(("swap", self.player, new_creature))
                    break

    def opponent_turn(self):
        choices = [Button("Attack"), Button("Swap")]
        choice = self._wait_for_choice(self.opponent, choices)

        if choice.display_name == "Attack":
            skill = self.choose_skill(self.opponent)
            if skill:
                self.turn_queue.append(("skill", self.opponent, skill))
        else:
            new_creature = self.choose_creature(self.opponent)
            if new_creature:
                self.turn_queue.append(("swap", self.opponent, new_creature))

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

    def resolve_turn(self):
        self.turn_queue.sort(key=lambda x: (-1 if x[0] == "swap" else x[1].active_creature.speed), reverse=True)

        for action in self.turn_queue:
            action_type, player, target = action
            if action_type == "swap" and target:
                player.active_creature = target
                self._show_text(self.player, f"{player.display_name} swapped to {target.display_name}!")
            elif action_type == "skill" and target:
                defender = self.player if player == self.opponent else self.opponent
                self.execute_skill(player, defender, target)

        self.turn_queue.clear()

    def execute_skill(self, attacker, defender, skill):
        if not skill:
            return
        target = defender.active_creature
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / target.sp_defense) * skill.base_damage

        effectiveness = self.get_effectiveness(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * effectiveness)
        target.hp = max(0, target.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender.display_name}'s {target.display_name}!")

        if target.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {target.display_name} fainted!")
            self.force_swap(defender)

    def get_effectiveness(self, skill_type, creature_type):
        effectiveness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return

        choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self.battle_ended = False
        self.turn_queue.clear()
