def __init__(self, app, player):
    super().__init__(app, player)
    self.bot = app.create_bot("basic_opponent")
    
    # Reset creatures HP to max_hp
    for creature in self.player.creatures:
        creature.hp = creature.max_hp
    for creature in self.bot.creatures:
        creature.hp = creature.max_hp
        
    # Set initial active creatures
    self.player.active_creature = self.player.creatures[0]
    self.bot.active_creature = self.bot.creatures[0]
