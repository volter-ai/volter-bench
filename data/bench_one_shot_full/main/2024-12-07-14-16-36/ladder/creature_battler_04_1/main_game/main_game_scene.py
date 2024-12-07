# Reset creatures before leaving
self.player_creature.hp = self.player_creature.max_hp
self.bot_creature.hp = self.bot_creature.max_hp
self._transition_to_scene("MainMenuScene")
