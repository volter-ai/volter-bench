import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player, bot):
        super().__init__(app, player)
        self.bot = bot
        self.initialize_battle()

    def initialize_battle(self):
        self.reset_creatures()
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.bot.display_name}: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        self.battle_loop()
        self.reset_creatures()

    def battle_loop(self):
        while True:
            player_action = self.player_choice_phase()
            bot_action = self.bot_choice_phase()
            self.resolution_phase(player_action, bot_action)

            if self.check_battle_end():
                break

    def player_choice_phase(self):
        action_queue = []
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill = self.choose_attack(self.player)
                if skill:
                    action_queue.append(("attack", skill))
                    return action_queue
            elif swap_button == choice:
                creature = self.choose_swap(self.player)
                if creature:
                    action_queue.append(("swap", creature))
                    return action_queue

    def bot_choice_phase(self):
        action_queue = []
        while True:
            choice = random.choice(["Attack", "Swap"])
            if choice == "Attack":
                skill = self.choose_attack(self.bot)
                if skill:
                    action_queue.append(("attack", skill))
                    return action_queue
            else:
                creature = self.choose_swap(self.bot)
                if creature:
                    action_queue.append(("swap", creature))
                    return action_queue

    def choose_attack(self, actor: Player):
        choices = [SelectThing(skill) for skill in actor.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        choice = self._wait_for_choice(actor, choices)
        if choice == back_button:
            return None
        return choice.thing

    def choose_swap(self, actor: Player):
        available_creatures = [c for c in actor.creatures if c != actor.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(actor, "No creatures available to swap!")
            return None
        choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        choice = self._wait_for_choice(actor, choices)
        if choice == back_button:
            return None
        return choice.thing

    def resolution_phase(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Resolve swaps first
        for actor, action_queue in actions:
            if action_queue[0][0] == "swap":
                self.swap_creature(actor, action_queue[0][1])

        # Resolve attacks
        attack_actions = [(actor, action_queue[0][1]) for actor, action_queue in actions if action_queue[0][0] == "attack"]
        attack_actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if len(attack_actions) == 2 and attack_actions[0][0].active_creature.speed == attack_actions[1][0].active_creature.speed:
            random.shuffle(attack_actions)
        for actor, skill in attack_actions:
            self.execute_skill(actor, skill)

    def swap_creature(self, actor: Player, new_creature: Creature):
        actor.active_creature = new_creature
        self._show_text(actor, f"{actor.display_name} swapped to {new_creature.display_name}!")

    def execute_skill(self, actor: Player, skill: Skill):
        target = self.bot if actor == self.player else self.player
        damage = self.calculate_damage(actor.active_creature, target.active_creature, skill)
        target.active_creature.hp = max(0, target.active_creature.hp - damage)
        self._show_text(actor, f"{actor.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type: str, defender_type: str):
        effectiveness = {
            "normal": {},
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True

        if self.player.active_creature.hp == 0:
            self.force_swap(self.player)
        if self.bot.active_creature.hp == 0:
            self.force_swap(self.bot)

        return False

    def force_swap(self, actor: Player):
        available_creatures = [c for c in actor.creatures if c.hp > 0]
        if available_creatures:
            new_creature = random.choice(available_creatures)
            self.swap_creature(actor, new_creature)
        else:
            self._show_text(actor, f"{actor.display_name} has no more creatures able to battle!")

    def reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
