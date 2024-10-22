from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, BotListener
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self._player_turn()
            self._bot_turn()
            if self._resolve_turn():
                break
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill = self._choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("skill", self.player, skill))
                    break
            elif swap_button == choice:
                new_creature = self._choose_creature(self.player)
                if new_creature:
                    self.turn_queue.append(("swap", self.player, new_creature))
                    break

    def _bot_turn(self):
        bot_choice = random.choice(["Attack", "Swap"])
        if bot_choice == "Attack":
            skill = random.choice(self.bot.active_creature.skills)
            self.turn_queue.append(("skill", self.bot, skill))
        else:
            available_creatures = [c for c in self.bot.creatures if c != self.bot.active_creature and c.hp > 0]
            if available_creatures:
                new_creature = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.bot, new_creature))
            else:
                skill = random.choice(self.bot.active_creature.skills)
                self.turn_queue.append(("skill", self.bot, skill))

    def _resolve_turn(self):
        self.turn_queue.sort(key=lambda x: (-1 if x[0] == "swap" else x[1].active_creature.speed), reverse=True)

        for action, player, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "skill":
                self._execute_skill(player, target)

            if self._check_battle_end():
                return True

        self.turn_queue.clear()
        return False

    def _execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} fainted!")
            self._force_swap(defender)

    def _get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, creature_type), 1)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            new_creature = self._choose_creature(player, force=True)
            if new_creature:
                player.active_creature = new_creature
                self._show_text(player, f"{player.display_name} sent out {new_creature.display_name}!")
            else:
                self._show_text(player, f"{player.display_name} has no more creatures able to battle!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def _check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        if all(c.hp == 0 for c in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def _choose_skill(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_creature(self, player, force=False):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures]
        if not force:
            choices.append(Button("Back"))
        
        if isinstance(player._listener, BotListener):
            return random.choice(available_creatures) if available_creatures else None
        
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None
