export const INITIAL_VALUES = {
  TANK_COUNT: 1,
  TANK_DAMAGE: 10,
  FIRE_RATE: 1,
  TANK_HEALTH: 100,
  TANK_RANGE: 200,
  TANK_SPEED: 200,
  PROJECTILE_SPEED: 300,
  ENEMY_COUNT: 3,
  CREDITS_PER_KILL: 10,
  COLLISION_RADIUS: 32
};

export const UPGRADE_COSTS = {
  TANK_COUNT: 100,
  TANK_DAMAGE: 50,
  FIRE_RATE: 75,
  TANK_HEALTH: 60,
  TANK_RANGE: 80
};

export const BATTLE_POSITIONS = {
  FRIENDLY: [
    {x: 200, y: 150},
    {x: 200, y: 300},
    {x: 200, y: 450},
    {x: 150, y: 200},
    {x: 150, y: 350}
  ],
  ENEMY: [
    {x: 600, y: 150},
    {x: 600, y: 300},
    {x: 600, y: 450},
    {x: 650, y: 200},
    {x: 650, y: 350}
  ]
};
