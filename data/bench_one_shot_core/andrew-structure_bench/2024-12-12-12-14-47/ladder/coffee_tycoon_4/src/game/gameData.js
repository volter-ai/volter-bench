export const INITIAL_VALUES = {
  MONEY: 0,
  BARISTA_COUNT: 1,
  BARISTA_SPEED: 1,
  CUSTOMER_CAPACITY: 3,
  COFFEE_PRICE: 5,
  PROCESSING_SPEED: 1.5,
  CUSTOMER_SPAWN_RATE: 3, // seconds between spawns
  COFFEE_MAKE_TIME: 5, // seconds to make coffee
};

export const UPGRADE_COSTS = {
  BARISTA: 100,
  BARISTA_SPEED: 150,
  CUSTOMER_CAPACITY: 200,
  COFFEE_PRICE: 250,
  PROCESSING_SPEED: 300,
};

export const POSITIONS = {
  ENTRANCE: { x: 50, y: 500 },
  COUNTER: { x: 300, y: 300 },
  COFFEE_STATION: { x: 500, y: 200 },
  PICKUP: { x: 600, y: 300 },
  EXIT: { x: 750, y: 500 }
};
