export const INITIAL_VALUES = {
  BARISTA_COUNT: 1,
  MACHINE_COUNT: 1,
  BARISTA_SPEED: 150, // Increased from 100
  MAX_CUSTOMERS: 5,
  COFFEE_QUALITY: 1,
  COFFEE_PREP_TIME: 2, // Reduced from 3
  CUSTOMER_SPAWN_TIME: 1, // Reduced from 2
  CUSTOMER_PATIENCE: 20, // seconds
  BASE_COFFEE_PRICE: 8,
};

export const UPGRADE_COSTS = {
  BARISTA: 12,  // Reduced from 15
  MACHINE: 15,  // Reduced from 20
  SPEED: 12,    // Reduced from 15
  SPACE: 20,    // Reduced from 25
  QUALITY: 15,  // Reduced from 20
};

export const POSITIONS = {
  ENTRANCE: { x: 50, y: 500 },
  COUNTER: { x: 300, y: 300 },
  EXIT: { x: 750, y: 500 },
  MACHINE_START: { x: 500, y: 100 },
  MACHINE_SPACING: 100,
};
