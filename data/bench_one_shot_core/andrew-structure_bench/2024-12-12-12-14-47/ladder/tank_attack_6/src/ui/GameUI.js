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
    {children} ({cost} credits)
  </button>
);

const HUD = ({ game }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '10px', backgroundColor: 'rgba(0,0,0,0.5)', color: '#d3d3d3' }}>
    <p>Credits: {game.credits} | Tanks: {game.tankCount} | Speed: {game.tankSpeed.toFixed(1)} | Health: {game.tankHealth.toFixed(0)} | Damage: {game.tankDamage.toFixed(1)} | Fire Rate: {game.tankFireRate.toFixed(1)} | Range: {game.tankRange.toFixed(0)}</p>
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
        <Button onClick={() => game.upgradeTankCount()} cost={game.tankCountCost}>Add Tank</Button>
        <Button onClick={() => game.upgradeTankSpeed()} cost={game.tankSpeedCost}>Upgrade Speed</Button>
        <Button onClick={() => game.upgradeTankHealth()} cost={game.tankHealthCost}>Upgrade Health</Button>
        <Button onClick={() => game.upgradeTankDamage()} cost={game.tankDamageCost}>Upgrade Damage</Button>
        <Button onClick={() => game.upgradeTankFireRate()} cost={game.tankFireRateCost}>Upgrade Fire Rate</Button>
        <Button onClick={() => game.upgradeTankRange()} cost={game.tankRangeCost}>Upgrade Range</Button>
      </div>
    </div>
  );
};

export default GameUI;
