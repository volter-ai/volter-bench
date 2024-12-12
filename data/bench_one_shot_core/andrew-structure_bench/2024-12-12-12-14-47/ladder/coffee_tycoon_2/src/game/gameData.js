export const INITIAL_VALUES = {
  BARISTA_SPEED: 200, // pixels per second
  BARISTA_COUNT: 1,
  COFFEE_PREP_TIME: 3, // seconds
  SERVICE_TIME: 2, // seconds
  COUNTER_COUNT: 1,
  PAYMENT_AMOUNT: 20, // Changed from 10 to 20
};

export const UPGRADE_COSTS = {
  BARISTA: 25, // Changed from 50
  BARISTA_SPEED: 15, // Changed from 30
  COFFEE_MACHINE: 20, // Changed from 40
  COUNTER: 30, // Changed from 60
  PREMIUM_PRICES: 35, // Changed from 75
  TRAINING: 20, // Changed from 45
};

export const STATION_POSITIONS = {
  IDLE_POSITION: { x: 400, y: 500 },
  COFFEE_MACHINES: [
    { x: 200, y: 300 },
    { x: 300, y: 300 },
    { x: 400, y: 300 }
  ],
  ORDER_COUNTERS: [
    { x: 200, y: 100 },
    { x: 300, y: 100 },
    { x: 400, y: 100 }
  ],
  SERVICE_COUNTERS: [
    { x: 600, y: 100 },
    { x: 600, y: 200 },
    { x: 600, y: 300 }
  ]
};
