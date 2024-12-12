export const INITIAL_VALUES = {
  COFFEE_MAKE_SPEED: 3, // seconds to make coffee
  BARISTA_SPEED: 100, // pixels per second
  CUSTOMER_SPEED: 80, // pixels per second
  COFFEE_PRICE: 5,
  BARISTA_COUNT: 1,
  CUSTOMER_CAPACITY: 3,
  BARISTA_EFFICIENCY: 1, // coffees carried at once
};

export const UPGRADE_COSTS = {
  COFFEE_SPEED: 10,
  BARISTA_COUNT: 25,
  CUSTOMER_CAPACITY: 15,
  COFFEE_PRICE: 20,
  BARISTA_EFFICIENCY: 30,
};

export const LOCATIONS = {
  ENTRANCE: { x: 50, y: 300 },
  EXIT: { x: 750, y: 300 },
  REGISTER: { x: 600, y: 300 },
  COUNTER: { x: 400, y: 300 },
  COFFEE_STATIONS: [
    { x: 200, y: 150 },
    { x: 200, y: 300 },
    { x: 200, y: 450 },
  ]
};
