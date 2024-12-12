import React, { useState, useEffect } from 'react';

const Button = ({ onClick, children, cost }) => (
  <button onClick={onClick} style={{
    margin: '5px',
    padding: '5px 10px',
    fontSize: '14px',
    color: '#d3d3d3',
    border: 'none',
    cursor: 'pointer',
    backgroundColor: '#7C45CB',
    position: 'relative',
  }}>
    {children} ({cost} crystals)
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#d3d3d3' }}>
    <p>Crystals: {Math.floor(game.crystals)} | Drones: {game.droneCount} | Mining Speed: {game.miningSpeed.toFixed(1)}s | Cargo: {game.cargoCapacity} | Asteroids: {game.asteroidLimit} | Crystal Density: {game.crystalDensity}</p>
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
    <div style={{ width: '100%', height: '100%', color: '#d3d3d3' }}>
      <HUD game={game} />
      <div style={{ position: 'absolute', bottom: '10px', left: '10px', right: '10px', textAlign: 'center' }}>
        <Button onClick={() => game.upgradeDroneCount()} cost={game.droneCost}>Add Drone</Button>
        <Button onClick={() => game.upgradeMiningSpeed()} cost={game.miningSpeedCost}>Upgrade Mining Speed</Button>
        <Button onClick={() => game.upgradeCargoCapacity()} cost={game.cargoCapacityCost}>Upgrade Cargo Capacity</Button>
        <Button onClick={() => game.upgradeAsteroidLimit()} cost={game.asteroidLimitCost}>Increase Asteroid Limit</Button>
        <Button onClick={() => game.upgradeCrystalDensity()} cost={game.crystalDensityCost}>Increase Crystal Density</Button>
      </div>
    </div>
  );
};

export default GameUI;
