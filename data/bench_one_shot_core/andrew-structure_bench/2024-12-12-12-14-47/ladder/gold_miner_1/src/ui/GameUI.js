import React, { useState, useEffect } from 'react';

const Button = ({ onClick, children, cost, disabled }) => (
  <button 
    onClick={onClick} 
    disabled={disabled}
    style={{
      margin: '5px',
      padding: '5px 10px',
      fontSize: '14px',
      backgroundColor: disabled ? '#666' : '#4CAF50',
      color: 'white',
      border: 'none',
      cursor: disabled ? 'not-allowed' : 'pointer',
    }}
  >
    {children} ({cost} crystals)
  </button>
);

const HUD = ({ game }) => (
  <div style={{ 
    position: 'absolute', 
    top: 0, 
    left: 0, 
    right: 0, 
    padding: '10px', 
    backgroundColor: 'rgba(0,0,0,0.7)',
    color: 'white'
  }}>
    <p>Crystals: {Math.floor(game.crystals)}</p>
    <p>Ships: {game.miningShips} | Mining Speed: {game.miningSpeed.toFixed(1)}s | 
       Cargo: {game.cargoCapacity} | Asteroids: {game.maxAsteroids} | 
       Crystal Density: {game.crystalDensity}</p>
  </div>
);

const GameUI = ({ gameRef }) => {
  const [, forceUpdate] = useState();
  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 100);
    return () => clearInterval(interval);
  }, []);

  if (!gameRef.current) return null;

  const game = gameRef.current;

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <HUD game={game} />
      <div style={{ 
        position: 'absolute', 
        bottom: '10px', 
        left: '10px', 
        right: '10px', 
        textAlign: 'center' 
      }}>
        <Button 
          onClick={() => game.upgradeMiningShips()} 
          cost={game.miningShipsCost}
          disabled={game.crystals < game.miningShipsCost}
        >
          Add Mining Ship
        </Button>
        <Button 
          onClick={() => game.upgradeMiningSpeed()} 
          cost={game.miningSpeedCost}
          disabled={game.crystals < game.miningSpeedCost}
        >
          Upgrade Mining Speed
        </Button>
        <Button 
          onClick={() => game.upgradeCargoCapacity()} 
          cost={game.cargoCapacityCost}
          disabled={game.crystals < game.cargoCapacityCost}
        >
          Upgrade Cargo Capacity
        </Button>
        <Button 
          onClick={() => game.upgradeMaxAsteroids()} 
          cost={game.maxAsteroidsCost}
          disabled={game.crystals < game.maxAsteroidsCost}
        >
          Add Asteroid
        </Button>
        <Button 
          onClick={() => game.upgradeCrystalDensity()} 
          cost={game.crystalDensityCost}
          disabled={game.crystals < game.crystalDensityCost}
        >
          Upgrade Crystal Density
        </Button>
      </div>
    </div>
  );
};

export default GameUI;
