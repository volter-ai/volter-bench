export const INITIAL_VALUES = {
  BARISTA_SPEED: 100, // pixels per second
  COFFEE_MAKE_TIME: 3, // seconds to make coffee
  COFFEE_PRICE: 10,  // Changed from 5 to 10
  CUSTOMER_CAPACITY: 3,
  BARISTA_COUNT: 1,
};

export const UPGRADE_COSTS = {
  BARISTA: 50,
  SPEED: 20,         // Changed from 30 to 20
  COFFEE_EFFICIENCY: 40,
  CAPACITY: 15,      // Changed from 25 to 15
  PRICE: 25,         // Changed from 35 to 25
};

export const POSITIONS = {
  COFFEE_MACHINE: { x: 400, y: 300 },
  CUSTOMER_COUNTER: { x: 100, y: 300 },
  SERVING_COUNTER: { x: 700, y: 300 },
  CUSTOMER_SPACING: 80,
};

export const MOVEMENT_POINTS = {
  START: { x: 300, y: 300 },
  COFFEE_MACHINE: { x: 400, y: 300 },
  SERVING: { x: 700, y: 300 },
};
