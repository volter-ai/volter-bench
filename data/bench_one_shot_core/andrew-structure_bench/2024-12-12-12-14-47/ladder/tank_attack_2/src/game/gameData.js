export const INITIAL_VALUES = {
  TANK_HEALTH: 150,
  TANK_DAMAGE: 50,
  TANK_SPEED: 100,
  TANK_COUNT: 1,
  BASE_REWARD: 20,
  BASE_HEALTH: 100,
  BASE_DAMAGE: 5,
  TANK_SPAWN_TIME: 3,
  BASE_SPAWN_TIME: 5
};

export const UPGRADE_COSTS = {
  TANK_HEALTH: 5,
  TANK_DAMAGE: 8,
  TANK_SPEED: 10,
  TANK_COUNT: 25,
  BASE_REWARD: 15
};

export const SPAWN_POSITIONS = {
  TANKS: [
    {x: 50, y: 100},
    {x: 50, y: 300},
    {x: 50, y: 500}
  ],
  BASES: [
    {x: 700, y: 150},
    {x: 700, y: 300},
    {x: 700, y: 450}
  ]
};
