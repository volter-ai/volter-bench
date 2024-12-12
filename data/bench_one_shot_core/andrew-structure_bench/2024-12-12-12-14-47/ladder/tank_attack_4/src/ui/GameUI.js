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
  }}>
    {children} ({cost} credits)
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#d3d3d3' }}>
    <p>Credits: {Math.floor(game.credits)} | Tanks: {game.tankCount} | Damage: {Math.floor(game.tankDamage)} | Speed: {Math.floor(game.tankSpeed)} | Range: {Math.floor(game.tankRange)} | Armor: {Math.floor(game.tankArmor)} | Spawn Rate: {game.enemySpawnRate.toFixed(1)}/s</p>
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
        <Button onClick={() => game.upgradeTankSpeed()} cost={game.tankSpeedCost}>Upgrade Tank Speed</Button>
        <Button onClick={() => game.upgradeTankDamage()} cost={game.tankDamageCost}>Upgrade Tank Damage</Button>
        <Button onClick={() => game.upgradeTankRange()} cost={game.tankRangeCost}>Upgrade Tank Range</Button>
        <Button onClick={() => game.upgradeTankArmor()} cost={game.tankArmorCost}>Upgrade Tank Armor</Button>
        <Button onClick={() => game.upgradeTankCount()} cost={game.tankCountCost}>Add Tank</Button>
        <Button onClick={() => game.upgradeEnemySpawnRate()} cost={game.enemySpawnRateCost}>Increase Enemy Spawn Rate</Button>
      </div>
    </div>
  );
};

export default GameUI;
